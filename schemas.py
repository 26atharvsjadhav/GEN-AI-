# schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class WebsiteRequest(BaseModel):
    website_url: str

class FAQ(BaseModel):
    question: str
    answer: str

class BrandInsights(BaseModel):
    product_catalog: Dict[str, Any]
    hero_products: List[str]
    privacy_policy: Optional[str]
    return_policy: Optional[str]
    faqs: List[FAQ]
    social_links: List[str]
    contacts: List[str]
    about: Optional[str]
    important_links: List[str]
