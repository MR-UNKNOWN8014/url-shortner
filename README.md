# URL Shortener API

> A production-ready URL shortening service with a real-time analytics dashboard — built with FastAPI, SQLite, and vanilla JS.

Paste a long URL, get a short code back, share it, and watch the click counter go up. Every redirect is tracked. Every stat is live.

---

## Overview

This project is a fully functional URL shortener REST API with a built-in analytics dashboard. Short codes are:

- **6 characters** - randomly generated using Python's `secrets` module
- **Collision-safe** - verified unique against the database before being issued
- **Persistent** - stored in SQLite, survives server restarts
- **Tracked** - every redirect increments a click counter in real time

The dashboard at `/dashboard` shows all links, total clicks, the top-performing URL, and ability to search records by URL or `Short_code` - no page refresh needed.

---

## Tech Stack

|Layer|Technology|
|---|---|
|Framework|FastAPI 0.115.0|
|Server|Uvicorn 0.30.6|
|Database|SQLite 3 (built-in)|
|Validation|Pydantic v2|
|Frontend|Vanilla HTML / CSS / JS|
|Language|Python 3.11+|

---

## Project Structure

```
url-shortener/
├── main.py              # FastAPI app and route definitions
├── models.py            # Pydantic request/response schemas
├── database.py          # SQLite connection and query functions
├── shortener.py         # Short code generation logic
├── requirements.txt     # Project dependencies
├── static/
│   └── dashboard.html   # Analytics dashboard (served at /dashboard)
├── urls.db              # Auto-created SQLite database (gitignored)
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MR-UNKNOWN8014/url-shortener.git
cd url-shortener
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

Server starts at `http://localhost:8000`

### 5. Open the dashboard

```
http://localhost:8000/dashboard
```

### 6. Explore the interactive API docs

```
http://localhost:8000/docs
```

---

## API Endpoints

|Method|Endpoint|Description|
|---|---|---|
|`GET`|`/`|Health check|
|`POST`|`/shorten`|Shorten a long URL|
|`GET`|`/s/{short_code}`|Redirect to original URL|
|`GET`|`/stats/{short_code}`|Get click stats for a short code|
|`GET`|`/urls`|List all shortened URLs with stats|
|`GET`|`/dashboard`|Analytics dashboard UI|

---

## Usage Examples

### Health Check

```bash
GET http://localhost:8000/
```

```json
{
  "status": "running",
  "message": "URL Shortener API is live 🚀"
}
```

---

### Shorten a URL

```bash
POST http://localhost:8000/shorten
Content-Type: application/json

{
  "original_url": "https://github.com"
}
```

```json
{
  "short_code": "aB3xQz",
  "short_url": "http://localhost:8000/s/aB3xQz",
  "original_url": "https://github.com"
}
```

---

### Redirect

```
GET http://localhost:8000/s/aB3xQz
```

Returns HTTP `307 Temporary Redirect` — browser lands on the original URL. Click count increments automatically.

---

### Get Click Stats

```bash
GET http://localhost:8000/stats/aB3xQz
```

```json
{
  "original_url": "https://github.com",
  "short_code": "aB3xQz",
  "click_count": 5
}
```

---

### List All URLs

```bash
GET http://localhost:8000/urls
```

```json
[
  {
    "short_code": "aB3xQz",
    "original_url": "https://github.com",
    "click_count": 5
  },
  {
    "short_code": "mK9pLr",
    "original_url": "https://fastapi.tiangolo.com",
    "click_count": 2
  }
]
```

---

## Dashboard

Visit `http://localhost:8000/dashboard` for the live analytics UI.

**Features**:

- Total links created and total clicks across all URLs
- Top-performing link highlighted by click count
- Full links table sorted by most visited
- Shorten new URLs directly from the dashboard
- One-click copy for any short link
- Auto-refreshes every 15 seconds

---

## Error Handling

|Status Code|Scenario|
|---|---|
|`404 Not Found`|Short code does not exist in the database|
|`422 Unprocessable Entity`|Invalid or malformed URL submitted|
|`500 Internal Server Error`|Unexpected server-side failure|

**404 response:**

```json
{
  "detail": "Short URL not found"
}
```

**422 response (invalid URL):**

```json
{
  "detail": [
    {
      "type": "url_parsing",
      "loc": ["body", "original_url"],
      "msg": "Input should be a valid URL"
    }
  ]
}
```

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS urls (
    short_code   TEXT PRIMARY KEY,
    original_url TEXT NOT NULL,
    click_count  INTEGER DEFAULT 0
);
```

The `urls.db` file is auto-created on first startup via `init_db()`. No manual database setup required.

---

## Key Design Decisions

**Collision-safe code generation** - `shortener.py` loops until it finds a short code not already in the database. With 64⁶ (~68 billion) possible combinations at 6 characters, collisions are statistically rare but handled correctly regardless.

**SQL injection prevention** - all database queries use `?` parameterized placeholders. No f-strings or string concatenation are used in SQL statements.

**Separated concerns** - database logic, code generation, validation schemas, and route handlers each live in their own module. Swapping SQLite for PostgreSQL or Redis only requires changes inside `database.py`.

**Pydantic `HttpUrl` validation** - invalid URLs are rejected automatically at the request boundary before any application logic runs, returning a structured 422 error with no extra code required.

---
