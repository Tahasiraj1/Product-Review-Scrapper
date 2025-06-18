import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_reviews(url: str) -> List[Dict]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    reviews = []
    review_containers = soup.select('div.mod-reviews div.item')
    
    for container in review_containers:
        try:
            product_name = soup.select_one('h1.title').text.strip() if soup.select_one('h1.title') else "Unknown"
            review_text = container.select_one('div.review-content').text.strip()
            rating = float(container.select_one('div.review-rate').get('data-rate', '0'))
            
            reviews.append({
                'product_name': product_name,
                'review_text': review_text,
                'rating': rating
            })
        except:
            continue
    
    return reviews