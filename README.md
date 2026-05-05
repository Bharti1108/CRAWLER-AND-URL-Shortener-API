#  Assignment 1 URL-Shortener-API

## Features
- Shorten long URLs
- Redirect using short code
- SQLite database with SQLAlchemy

## How to run

pip install -r requirements.txt
uvicorn main:app --reload

## Endpoints
POST /shorten
GET /{code}


# Assignment 2 - Web Phone Number Crawler

## Description
This project crawls a website and extracts Indian phone numbers from pages within the same domain.

## Features
- BFS crawling (queue-based)
- Extracts Indian phone numbers using regex
- Normalizes phone numbers
- Avoids external domains
- Rate limiting (delay between requests)

## How to run

pip install -r requirements.txt
python main.py
