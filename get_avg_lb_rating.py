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

def get_letterboxd_genres(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script", type="application/ld+json")
    if not script:
        return None
    cleaned = re.sub(r'/\*.*?\*/', '', script.string, flags=re.DOTALL).strip()
    data = json.loads(cleaned)
    return data.get("genre")

def get_letterboxd_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script", type="application/ld+json")
    if not script:
        return None
    cleaned = re.sub(r'/\*.*?\*/', '', script.string, flags=re.DOTALL).strip()
    data = json.loads(cleaned)
    return {
        "title": data.get("name"),
        "year": data.get("releasedEvent", [{}])[0].get("startDate"),
        "rating": data.get("aggregateRating", {}).get("ratingValue"),
        "genres": data.get("genre"),
        "director": [d.get("name") for d in data.get("director", [])],
        "actors": [d.get("name") for d in data.get("actors", [])],
    }

#print(get_letterboxd_rating("https://boxd.it/72s"))
#print(get_letterboxd_genres("https://boxd.it/72s"))
print(get_letterboxd_data("https://boxd.it/72s"))