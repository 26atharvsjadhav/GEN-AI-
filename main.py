from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
import re
from parsers import extract_faqs, extract_about_text
from utils import make_absolute
from parsers import  extract_hero_products,extract_faqs
from schemas import BrandInsights, FAQ
from competitor_fetcher import fetch_competitor_insights
from typing import Dict, Any
from fetch_logic import fetch_insights_logic







app = FastAPI()

class WebsiteRequest(BaseModel):
    website_url: str

@app.post("/fetch-insights")
async def fetch_insights(request_data: WebsiteRequest):
    url = request_data.website_url.rstrip("/")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Check website status
            homepage_response = await client.get(url)
            if homepage_response.status_code != 200:
                raise HTTPException(status_code=401, detail="Website not reachable")

            homepage_soup = BeautifulSoup(homepage_response.text, "html.parser")
            hero_products = extract_hero_products(homepage_soup, url)
            social_links = extract_social_links(homepage_soup) 
            

            faqs = extract_faqs(homepage_soup)

            about = extract_about_text(homepage_soup)


            # 1. Fetch Product Catalog
            products_response = await client.get(f"{url}/products.json")
            if products_response.status_code == 200:
                raw_products = products_response.json().get("products", [])
                products_data = [clean_product(p) for p in raw_products]
            else:
                products_data = []

            # 2. Hero Products - Find product links/images on homepage
            hero_products = []
            for product_tag in homepage_soup.find_all("a", href=True):
                if "/products/" in product_tag['href']:
                    hero_products.append(product_tag['href'])

            # 3. Privacy Policy (Try common link patterns)
            privacy_policy = await fetch_common_page(client, url, "privacy-policy")

            # 4. Return/Refund Policy
            return_policy = await fetch_common_page(client, url, "refund-policy")

            # 5. FAQs (Try guessing page or extract FAQ from homepage)
            faqs = await fetch_common_page(client, url, "faqs")

            # 6. Social Handles (Extract all links with known domains)
            social_links = extract_social_links(homepage_soup)

            # 7. Contact Details
            contacts = extract_contacts(homepage_soup)

            # 8. About Text (Extract if available)
            about = extract_about_text(homepage_soup)

            # 9. Important Links
            important_links = extract_important_links(homepage_soup)

            return BrandInsights(
    product_catalog={"products": products_data},  # <-- dictionary!
    hero_products=hero_products,
    privacy_policy=privacy_policy,
    return_policy=return_policy,
    faqs=[FAQ(**faq) for faq in (faqs or [])],
    social_links=social_links,
    contacts=contacts,
    about=about,
    important_links=important_links
)
        db = SessionLocal()
        try:
            brand_entry = BrandData(website_url=url, data=result.dict())
            db.add(brand_entry)
            db.commit()
        finally:
            db.close()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def fetch_common_page(client, url, page_slug):
    try:
        response = await client.get(f"{url}/policies/{page_slug}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(separator="\n", strip=True)
    except:
        pass
    return None


def extract_social_links(soup):
    social_platforms = ['facebook', 'instagram', 'twitter', 'tiktok', 'youtube', 'linkedin']
    links = []
    for a in soup.find_all('a', href=True):
        if any(platform in a['href'].lower() for platform in social_platforms):
            
            
            links.append(a['href'])
    return list(set(links))


def extract_contacts(soup):
    contacts = []
    text = soup.get_text(separator=" ")
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phones = re.findall(r"\+?\d[\d\s\-]{7,}\d", text)
    if emails:
        contacts.extend(emails)
    if phones:
        contacts.extend(phones)
    return contacts


def extract_about_text(soup):
    about_keywords = ["about", "who we are"]
    for section in soup.find_all(['section', 'div']):
        if any(keyword in section.get_text(separator=" ").lower() for keyword in about_keywords):
            return section.get_text(separator="\n", strip=True)
    return None


def extract_important_links(soup):
    keywords = ["contact", "order tracking", "blog"]
    links = []
    for a in soup.find_all('a', href=True):
        if any(kw in a.get_text().lower() for kw in keywords):
            links.append(a['href'])
    return list(set(links))


def clean_product(product):
    # Remove keys like 'body_html' and any other unwanted HTML fields
    return {k: v for k, v in product.items() if not k.endswith('_html')}


@app.post("/fetch-insights", response_model=BrandInsights)
async def fetch_insights(request_data: WebsiteRequest):
    try:
        return await fetch_insights_logic(request_data.website_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fetch-competitor-insights")
async def fetch_competitors(request_data: WebsiteRequest):
    try:
        return await fetch_competitor_insights(request_data.website_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))