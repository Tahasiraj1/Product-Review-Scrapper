from fastapi.middleware.cors import CORSMiddleware
from google_sheets import save_to_google_sheets
from urllib.parse import urlparse, urlunparse
from fastapi import FastAPI, HTTPException
from processor import process_reviews
from scrapper import scrape_reviews
from pydantic import BaseModel
from ReviewModel import Review
from typing import List

def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(parsed._replace(query=""))

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape", response_model=List[Review])
async def scrape(request: ScrapeRequest):
    try:
        # Clean the URL
        url = clean_url(request.url)
        # Scrape reviews using Playwright
        reviews = await scrape_reviews(url, 5)
        # Process reviews (e.g., sentiment analysis)
        processed_reviews = process_reviews(reviews)
        # Save to Google Sheets
        save_to_google_sheets(processed_reviews)

        return processed_reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")