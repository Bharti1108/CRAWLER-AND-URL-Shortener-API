# URL-Shortener-API

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
