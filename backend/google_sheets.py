from typing import List
from ReviewModel import Review
import gspread
from auth import authenticate

@authenticate
def save_to_google_sheets(reviews: List[Review], creds=None):
    try:
        client = gspread.authorize(creds)

        sheet = client.open("Product Reviews").sheet1
        sheet.clear()

        sheet.append_row(['Product Name', 'Review Text', 'Rating', 'Sentiment'])

        for review in reviews:
            sheet.append_row([
                review.product_name,
                review.review_text,
                review.rating,
                review.sentiment
            ])
    except Exception as e:
        raise e

