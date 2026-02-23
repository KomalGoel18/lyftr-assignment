# Lyftr Assignment — Universal Website Scraper (FastAPI)

A small FastAPI service that **scrapes a given URL and returns structured content** (page metadata + “sections” extracted from semantic HTML). It attempts a **static HTML fetch first**, and if the extracted text is too small it **falls back to rendering the page with Playwright** and performing basic interactions (click/scroll/pagination).

## What this provides

- **API**
  - `GET /healthz`: health check
  - `POST /scrape`: scrape a URL (JSON in, JSON out)
- **Web UI**
  - `GET /`: simple form to call `/scrape` and view JSON output in the browser

## How scraping works (high level)

- **Static scrape first**: fetches HTML via `httpx`, parses with BeautifulSoup (`lxml` parser), and extracts:
  - page meta: title, description, language, canonical
  - sections from semantic containers: `section`, `article`, `main`, `header`, `footer`
  - per section: headings, text, links, images, lists
  - `rawHtml` is truncated to **1000 chars** and marked via `truncated`
- **JS fallback** (when extracted text is small): uses Playwright (Chromium, headless) to:
  - wait for `networkidle`
  - click up to 3 buttons with labels containing keywords like `"more"`, `"show"`, `"tab"`
  - scroll 3 times
  - follow a “Next” pagination link up to a small depth
  - returns an `interactions` object (`clicks`, `scrolls`, `pages`)

More detail lives in `design_notes.md` and `capabilities.json`.

## Requirements

- **Python**: recommended **3.10+**
- **Playwright browsers**: installed via `python -m playwright install`

Python dependencies are listed in `requirements.txt`.

## Quickstart

### Windows (PowerShell)

```powershell
cd E:\Projects\lyftr-assignment

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

python -m playwright install

uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open:
- `http://localhost:8000/` (UI)
- `http://localhost:8000/docs` (Swagger / OpenAPI)

### macOS / Linux (bash)

You can use the provided `run.sh`:

```bash
./run.sh
```

Or run manually:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API usage

### Health check

```bash
curl http://localhost:8000/healthz
```

### Scrape a URL

```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://example.com\"}"
```

### Response shape (overview)

`POST /scrape` returns:

- `result.url`: requested URL
- `result.scrapedAt`: UTC timestamp
- `result.meta`: title/description/language/canonical
- `result.sections[]`: extracted semantic sections
- `result.interactions`: click/scroll/pagination actions (especially relevant for JS fallback)
- `result.errors[]`: currently returned as an empty list

## Project structure

- `app/main.py`: FastAPI app + routes
- `app/scraper/static.py`: static HTTP fetch + section extraction
- `app/scraper/js.py`: Playwright rendering + simple interactions
- `app/templates/index.html`: minimal UI
- `design_notes.md`: scraping strategy notes
- `capabilities.json`: feature flags/capabilities summary

