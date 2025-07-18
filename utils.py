# utils.py
from urllib.parse import urljoin

def make_absolute(base_url: str, link: str) -> str:
    return urljoin(base_url, link)