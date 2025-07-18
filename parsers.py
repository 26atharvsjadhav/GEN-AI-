import re
from bs4 import BeautifulSoup
from utils import make_absolute

def extract_hero_products(soup: BeautifulSoup, base_url: str):
    products = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "/products/" in href:
            absolute_link = make_absolute(base_url, href)
            products.append(absolute_link)
    return list(set(products))


def extract_social_links(soup: BeautifulSoup, base_url: str):
    social_platforms = ['facebook', 'instagram', 'twitter', 'tiktok', 'youtube']
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if any(platform in href.lower() for platform in social_platforms):
            links.append(make_absolute(base_url, href))
    return list(set(links))


def extract_contacts(soup: BeautifulSoup):
    contacts = []
    text = soup.get_text(separator=" ", strip=True)
    
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phones = re.findall(r"\+?\d[\d\s\-]{7,}\d", text)
    
    if emails:
        contacts.extend(emails)
    if phones:
        contacts.extend(phones)
    
    return list(set(contacts))


def extract_about_text(soup: BeautifulSoup):
    about_keywords = ["about us", "our story", "who we are"]
    for section in soup.find_all(['section', 'div', 'p']):
        section_text = section.get_text(separator=" ", strip=True).lower()
        if any(keyword in section_text for keyword in about_keywords):
            return section.get_text(separator=" ", strip=True)
    return None


def extract_important_links(soup: BeautifulSoup, base_url: str):
    keywords = ["contact", "order tracking", "blog", "track"]
    links = []
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True).lower()
        if any(kw in text for kw in keywords):
            absolute_link = make_absolute(base_url, a['href'])
            links.append(absolute_link)
    return list(set(links))


def extract_faqs(soup: BeautifulSoup):
    faqs = []
    for question_tag in soup.find_all(["h2", "h3", "strong"], string=re.compile(r"Q.*\?", re.IGNORECASE)):
        answer_tag = question_tag.find_next_sibling(["p", "div", "span"])
        faqs.append({
            "question": question_tag.get_text(strip=True),
            "answer": answer_tag.get_text(strip=True) if answer_tag else "Answer not found"
        })
    return faqs
