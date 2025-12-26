# Design Notes

## Static vs JS Fallback
- Strategy: Static scraping is attempted first. If extracted text length is too small (<1000 chars), the system falls back to JS rendering using Playwright.

## Wait Strategy for JS
- [x] Network idle
- [ ] Fixed sleep
- [ ] Wait for selectors
- Details: The page waits for network to become idle before extraction.

## Click & Scroll Strategy
- Click flows implemented: Clicking buttons containing keywords such as "more", "show", or "tab".
- Scroll / pagination approach: Scrolls the page 3 times and follows "Next" pagination links up to depth 3.
- Stop conditions: Max scroll = 3, max pages = 3.

## Section Grouping & Labels
- DOM is grouped using semantic tags: section, article, header, main, footer.
- Labels are taken from the first heading, otherwise derived from the first words of content.

## Noise Filtering & Truncation
- No aggressive noise filtering implemented.
- rawHtml is truncated at 1000 characters and marked with truncated flag.
