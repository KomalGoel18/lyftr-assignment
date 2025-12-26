from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def js_render(url: str):
    interactions = {
        "clicks": [],
        "scrolls": 0,
        "pages": [url]
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle")

        # Click "Load more" / tabs / buttons
        buttons = page.query_selector_all("button")
        for btn in buttons[:3]:
            try:
                label = btn.inner_text().strip()
                if any(k in label.lower() for k in ["more", "show", "tab"]):
                    btn.click()
                    interactions["clicks"].append(label)
                    page.wait_for_timeout(1500)
            except:
                pass

        # Scroll depth ≥ 3
        for _ in range(3):
            page.mouse.wheel(0, 3000)
            interactions["scrolls"] += 1
            page.wait_for_timeout(1500)

        # Pagination depth ≥ 3
        for _ in range(2):
            next_link = page.query_selector("a:has-text('Next'), a[rel='next']")
            if next_link:
                href = next_link.get_attribute("href")
                if href:
                    next_url = urljoin(page.url, href)
                    page.goto(next_url)
                    page.wait_for_load_state("networkidle")
                    interactions["pages"].append(next_url)

        html = page.content()
        browser.close()

    return html, interactions