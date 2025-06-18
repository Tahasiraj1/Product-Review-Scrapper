# main.py
import asyncio
import sys

# THIS MUST BE AT THE VERY TOP OF THE FILE
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        print("INFO: asyncio event loop policy set to WindowsSelectorEventLoopPolicy.")
    except RuntimeError as e:
        print(f"WARNING: Could not set event loop policy: {e}")
        # This might happen if the loop is already running, which can occur with reloaders.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google_sheets import save_to_google_sheets
from scrapper import scrape_reviews
from processor import process_reviews
from ReviewModel import Review
from typing import List
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"\n\n\nPython version: {sys.version}\n\n\n")
logger.info(f"\n\n\nEvent loop policy: {asyncio.get_event_loop_policy()}\n\n\n")

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
        logger.info(f"Starting scrape for URL: {request.url}")
        # Scrape reviews using Playwright
        reviews = await scrape_reviews(request.url, num_reviews_to_extract=50)
        logger.info(f"Scraped {len(reviews)} reviews")

        # Process reviews (e.g., sentiment analysis)
        processed_reviews = process_reviews(reviews)
        logger.info(f"Processed {len(processed_reviews)} reviews")

        # Save to Google Sheets
        save_to_google_sheets(processed_reviews)
        logger.info("Reviews saved to Google Sheets")

        return processed_reviews
    except Exception as e:
        logger.error(f"Error during scrape endpoint: {str(e)}")
        traceback.print_exc()  # Log full stack trace for debugging
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")