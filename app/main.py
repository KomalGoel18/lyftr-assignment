from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
from bs4 import BeautifulSoup

from app.scraper.static import static_scrape
from app.scraper.js import js_render

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


class ScrapeRequest(BaseModel):
    url: str


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/scrape")
def scrape(req: ScrapeRequest):

    # First: static scrape
    meta, sections = static_scrape(req.url)
    total_text = sum(len(s["content"]["text"]) for s in sections)

    interactions = {
        "clicks": [],
        "scrolls": 0,
        "pages": [req.url]
    }

    # Fallback to JS if content is weak
    if total_text < 1000:
        html, interactions = js_render(req.url)

        # Re-parse rendered HTML
        soup = BeautifulSoup(html, "lxml")
        meta, sections = static_scrape(req.url)

    return {
        "result": {
            "url": req.url,
            "scrapedAt": datetime.utcnow().isoformat() + "Z",
            "meta": meta,
            "sections": sections,
            "interactions": interactions,
            "errors": []
        }
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
