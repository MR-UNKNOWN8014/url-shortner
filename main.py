from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


from database import init_db, save_url, get_url, increment_clicks, get_all_urls
from shortener import generate_short_code
from models import ShortenRequest, ShortenResponse, URLStats

app = FastAPI(
    title="URL Shortener API",
    description="Shorten URLs and Track clicks",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the database once
@app.on_event("startup")
def startup_event():
    init_db()
    print("Database initialized successfully")

# POST /shorten - submit a long URL
# Returns a short code + full short URL
@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest):
    original_url = str(request.original_url)
    short_code = generate_short_code()

    save_url(short_code, original_url)

    return ShortenResponse(
        short_code=short_code,
        short_url= f"http://127.0.0.1:8000/s/{short_code}",
        original_url=original_url
    )

# GET /s/{short_code} - redirect to original
# Increments click count on every visit
@app.get("/s/{short_code}")
def redirect_url(short_code: str):
    record = get_url(short_code)

    if record is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    increment_clicks(short_code)

    return RedirectResponse(url=record["original_url"], status_code=307)


# GET /stats/{short_code} — view click stats
@app.get("/stats/{short_code}", response_model=URLStats)
def get_stats(short_code: str):
    record = get_url(short_code)

    if record is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return URLStats(
        original_url=record["original_url"],
        short_code=short_code,
        click_count=record["click_count"]
    )

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

@app.get("/urls")
def list_urls():
    return get_all_urls()

# GET Health check
@app.get("/")
def root():
    return {"status": "running", "message": "URL Shortener API is up"}