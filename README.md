# GenAI Brand Insights API

This project provides a FastAPI-based backend to fetch and analyze e-commerce brand data, including product catalog, hero products, policies, FAQs, social handles, contact details, about text, and important links. It also supports competitor insights.

## Features

- Fetch product catalog (excluding HTML fields)
- Extract hero products from homepage
- Get privacy and return/refund policies
- Extract FAQs in Q&A format
- Find social handles (Instagram, Facebook, etc.)
- Extract contact details (emails, phones)
- Get brand about text
- List important links (order tracking, blogs, etc.)
- Fetch competitor insights

## Project Structure

```
GenAI/
├── main.py
├── schemas.py
├── competitor_fetcher.py
├── fetch_logic.py
├── parsers.py
├── utils.py
├── competitors_list.py
├── requirements.txt
└── README.md
```

## Setup

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd GenAI
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the API**
   ```sh
   uvicorn main:app --reload
   ```

4. **API Docs**
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Example Usage

POST `/fetch-insights`
```json
{
  "website_url": "https://examplestore.com"
}
```

## Requirements

See `requirements.txt` for all dependencies.

---

# filepath: c:\Users\INDIA\Desktop\GenAI\requirements.txt
fastapi
uvicorn
httpx
beautifulsoup4
pydantic