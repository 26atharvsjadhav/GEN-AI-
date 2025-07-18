# fetch_logic.py

import httpx
from bs4 import BeautifulSoup
from schemas import BrandInsights, FAQ
from parsers import (
    extract_hero_products,
    extract_social_links,
    extract_contacts,
    extract_about_text,
    extract_important_links,
    extract_faqs
)

async def fetch_common_page(client, url, page_slug):
    try:
        response = await client.get(f"{url}/policies/{page_slug}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(separator="\n", strip=True)
    except:
        pass
    return None


async def fetch_insights_logic(url: str) -> BrandInsights:
    async with httpx.AsyncClient(timeout=10) as client:
        homepage_response = await client.get(url)
        if homepage_response.status_code != 200:
            raise Exception("Website not reachable")
        
        homepage_soup = BeautifulSoup(homepage_response.text, "html.parser")

        hero_products = extract_hero_products(homepage_soup, url)
        social_links = extract_social_links(homepage_soup, url)
        contacts = extract_contacts(homepage_soup)
        about = extract_about_text(homepage_soup)
        important_links = extract_important_links(homepage_soup, url)
        faqs_list = extract_faqs(homepage_soup)

        products_response = await client.get(f"{url}/products.json")
        products_data = products_response.json().get("products", []) if products_response.status_code == 200 else []

        privacy_policy = await fetch_common_page(client, url, "privacy-policy")
        return_policy = await fetch_common_page(client, url, "refund-policy")

        return BrandInsights(
            product_catalog={"products": products_data},
            hero_products=hero_products,
            privacy_policy=privacy_policy,
            return_policy=return_policy,
            faqs=[FAQ(**faq) for faq in (faqs_list or [])],
            social_links=social_links,
            contacts=contacts,
            about=about,
            important_links=important_links
        )
