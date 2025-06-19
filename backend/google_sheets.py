from ReviewModel import Review
from typing import List
import gspread

def save_to_google_sheets(reviews: List[Review]):
    try:
        client = gspread.service_account(filename='credentials.json')

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

