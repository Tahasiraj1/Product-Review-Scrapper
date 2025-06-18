from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google_sheets import save_to_google_sheets
from scrapper import scrape_reviews
from processor import process_reviews
from ReviewModel import Review
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape", response_model=List[Review])
async def scrape(request: ScrapeRequest):
    try:
        reviews = scrape_reviews(request.url)
        processed_reviews = process_reviews(reviews)
        save_to_google_sheets(processed_reviews)
        return processed_reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))