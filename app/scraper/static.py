import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def static_scrape(url: str):
    res = httpx.get(url, timeout=20)
    html = res.text
    soup = BeautifulSoup(html, "lxml")

    # ---- META ----
    title = soup.title.string.strip() if soup.title else ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"].strip() if desc_tag else ""
    lang = soup.html.get("lang") if soup.html else "en"
    canon_tag = soup.find("link", rel="canonical")
    canonical = canon_tag["href"] if canon_tag else None

    meta = {
        "title": title,
        "description": description,
        "language": lang,
        "canonical": canonical
    }

    sections = []
    for i, sec in enumerate(soup.find_all(["section", "article", "main", "header", "footer"])):
        text = sec.get_text(" ", strip=True)
        if not text:
            continue

        headings = [h.get_text(strip=True) for h in sec.find_all(["h1","h2","h3"])]
        links = [{"text": a.get_text(strip=True), "href": urljoin(url, a["href"])} for a in sec.find_all("a", href=True)]
        images = [{"src": urljoin(url, img["src"]), "alt": img.get("alt","")} for img in sec.find_all("img", src=True)]
        lists = [[li.get_text(strip=True) for li in ul.find_all("li")] for ul in sec.find_all("ul")]

        raw = str(sec)[:1000]

        sections.append({
            "id": f"section-{i}",
            "type": "section",
            "label": headings[0] if headings else text[:40],
            "sourceUrl": url,
            "content": {
                "headings": headings,
                "text": text,
                "links": links,
                "images": images,
                "lists": lists,
                "tables": []
            },
            "rawHtml": raw,
            "truncated": len(raw) >= 1000
        })

    return meta, sections