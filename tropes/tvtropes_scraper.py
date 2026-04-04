"""
TV Tropes Scraper
-----------------
Scrapes the trope names (words before the colon) from the bullet point list
under the main tropes header on a TV Tropes page.

The header text varies per page (e.g. "This Roaring Rampage of Tropes includes
examples of the following", "Tropes used in...", etc.), so the scraper finds it
dynamically rather than matching a fixed string.

Usage:
    python tvtropes_scraper.py <url> [<url> ...]

Examples:
    python tvtropes_scraper.py https://tvtropes.org/pmwiki/pmwiki.php/Film/KillBill
    python tvtropes_scraper.py https://tvtropes.org/pmwiki/pmwiki.php/Film/KillBill \
                               https://tvtropes.org/pmwiki/pmwiki.php/Film/Inception

Dependencies:
    pip install requests beautifulsoup4
"""

import re
import sys
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup


# TV Tropes blocks default Python/requests user-agents, so we spoof a browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://tvtropes.org/",
}

# Patterns that signal a "tropes list" header. We match case-insensitively.
TROPES_HEADER_PATTERNS = [
    r"tropes",          # catches "includes examples of the following", "Tropes used in", etc.
    r"trope",
    r"examples",
]


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch a TV Tropes page and return a BeautifulSoup object."""
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url, timeout=15)
    resp.raise_for_status() # turns HTTP error into a Python exception
    return BeautifulSoup(resp.text, "html.parser")


def find_tropes_header(soup: BeautifulSoup):
    """
    Return the first heading element whose text contains a tropes-related keyword.
    TV Tropes uses <h2> for major section headers inside the article body.
    Falls back to any tag with a matching id or class if no <h2> matches.
    """
    # The main article content lives in div.entry-content or div#main-article, so restrict the search to that
    article = soup.find("div", id="main-article") or soup.find("div", class_="entry-content") or soup

    for heading in article.find_all(["h2", "h3", "h4"]):
        text = heading.get_text(" ", strip=True)
        for pattern in TROPES_HEADER_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return heading

    return None  # header not found


def extract_trope_names(soup: BeautifulSoup, url: str) -> list[str]:
    """
    Locate the tropes section and extract the word(s) before the colon
    from each top-level bullet point.
    """
    header = find_tropes_header(soup)
    if header is None:
        #print(f"  [!] Could not find a tropes header on {url}", file=sys.stderr)
        return []

    header_text = header.get_text(" ", strip=True)
    #print(f"  [✓] Found header: \"{header_text}\"")

    # Collect all <li> elements that appear after the header.
    # TV Tropes wraps bullets in <ul> tags directly inside the article div.
    trope_names = []

    # Walk siblings after the header to find bullet lists
    for sibling in header.find_next_siblings():
        tag = sibling.name

        # Stop if we hit another major heading (new section)
        if tag in ("h2", "h3", "h4"):
            break

        if tag == "ul":
            for li in sibling.find_all("li", recursive=False):
                text = li.get_text(" ", strip=True)
                # Grab everything before the first colon
                if ":" in text:
                    name = text.split(":")[0].strip()
                    if name:
                        trope_names.append(name)

    # Fallback: TV Tropes sometimes uses a flat <ul> not directly after the header
    if not trope_names:
        article = soup.find("div", id="main-article") or soup
        for ul in article.find_all("ul"):
            # Only process lists that come after the header in document order
            if header in ul.find_all_previous():
                for li in ul.find_all("li", recursive=False):
                    text = li.get_text(" ", strip=True)
                    if ":" in text:
                        name = text.split(":")[0].strip()
                        if name:
                            trope_names.append(name)
                if trope_names:
                    break

    return trope_names


def scrape(url: str) -> list[str]:
    print(f"\nScraping: {url}")
    try:
        soup = fetch_page(url)
        tropes = extract_trope_names(soup, url)
        print(f"  Found {len(tropes)} trope name(s).")
        return tropes
    except requests.HTTPError as e:
        print(f"  [!] HTTP error: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  [!] Unexpected error: {e}", file=sys.stderr)
        return []


def main():
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python tvtropes_scraper.py <url> [<url> ...]")
        sys.exit(1)

    for i, url in enumerate(urls):
        tropes = scrape(url)
        if tropes:
            print("\nTrope names:")
            for name in tropes:
                print(f"  - {name}")

        # Be polite between requests
        if i < len(urls) - 1:
            time.sleep(1.5)


if __name__ == "__main__":
    main()