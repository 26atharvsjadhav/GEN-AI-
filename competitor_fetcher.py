# competitor_fetcher.py

from competitors_list import COMPETITORS
from schemas import BrandInsights, WebsiteRequest
from fetch_logic import fetch_insights_logic   # ✅ Import fetch logic here

async def get_competitors_for(brand_url: str):
    domain = brand_url.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
    return COMPETITORS.get(domain, [])

async def fetch_competitor_insights(brand_url: str):
    competitors = await get_competitors_for(brand_url)
    results = []

    if not competitors:
        return {"message": "No competitors found"}

    for competitor_url in competitors:
        try:
            insights = await fetch_insights_logic(f"https://{competitor_url}")
            results.append({
                "competitor": competitor_url,
                "insights": insights
            })
        except Exception as e:
            results.append({
                "competitor": competitor_url,
                "error": str(e)
            })

    return results
