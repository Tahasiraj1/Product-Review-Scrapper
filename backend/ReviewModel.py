from pydantic import BaseModel

class Review(BaseModel):
    product_name: str
    review_text: str
    rating: float
    sentiment: str