from analyzer import analyze_sentiment
from ReviewModel import Review
from typing import List, Dict
import re

def clean_text(text: str) -> str:
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_reviews(reviews: List[Dict]) -> List[Review]:
    processed_reviews = []

    for review in reviews:
        try:
            cleaned_text = clean_text(review['review_text'])
            sentiment = analyze_sentiment(cleaned_text)

            processed_review = Review(
                product_name=review['product_name'],
                review_text=cleaned_text,
                rating=review['rating'],
                sentiment=sentiment
            )

            processed_reviews.append(processed_review)
        except Exception as e:
            # You might want to log or skip individual errors
            continue

    return processed_reviews
