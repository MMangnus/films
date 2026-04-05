import requests
import json
import re
from bs4 import BeautifulSoup

def get_letterboxd_rating(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    script = soup.find("script", type="application/ld+json")
    if not script:
        return None
    cleaned = re.sub(r'/\*.*?\*/', '', script.string, flags=re.DOTALL).strip()
    data = json.loads(cleaned)
    rating = data.get("aggregateRating", {}).get("ratingValue")    

    return rating

print(get_letterboxd_rating("https://boxd.it/72s"))