## 🛒 Product Review Scraper

This tool scrapes product reviews from Daraz.pk using Playwright, performs sentiment analysis, and saves the results to a connected Google Sheet via the Google Sheets API.

## 🛠️ Setup Instructions

# 1. Clone the Repository
- git clone https://github.com/Tahasiraj1/Product-Review-Scrapper

- cd product-review-scraper

# 2. Set Up Google Sheets API (via Service Account)
- Go to Google Cloud Console

- Create a new project or use an existing one

- Navigate to: APIs & Services > Library

S- earch for and enable the Google Sheets API and Google Drive API

- Go to: APIs & Services > Credentials

- Click “Create Credentials” > Service Account

- Download the credentials.json file

- Save it in your project’s backend/ folder

- Go to Google Sheets and create a new spreadsheet

- Share your Google Sheet (where data will be saved) with the generated service account email (e.g., my-bot@my-project.iam.gserviceaccount.com) with Editor access

# 3. Backend (FastAPI)

- Make sure you have uv package manager installed

- Run command (uv venv)

- Activate the virtual environment (.venv\Scripts\activate) windows

- Install dependencies (uv pip install .)

- uvicorn main:app --host 0.0.0.0 --port 8000

# 4. Frontend (Next.js)

- Install dependencies (npm install)

- Run the development server (npm run dev)

- Open http://localhost:3000 in your browser

- Paste the url of any daraz product you want to scrape reviews of.

## The system will:

    - Scrape up to 50 reviews

    - Perform sentiment analysis

    - Save results to your connected Google Sheet