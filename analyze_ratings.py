'''

'''

import sys
import requests
import pandas as pd
from tvtropes_scraper import fetch_page, extract_trope_names

FILM_CATEGORIES = ["Film", "WesternAnimation", "Series", "Anime", "Manga"]
TVTROPES_BASE_URL = "https://tvtropes.org/pmwiki/pmwiki.php"
URL_SEP = "/"

def get_tropes_for_movies(movie_titles: list[str]) -> dict[str, list[str]]:
    'Read urls from column of csv, fetch page, and extract trope names for each movie.'

    tropes = {}
    for movie in movie_titles:
        print(movie)
        found = False
        for category in FILM_CATEGORIES:
            url = f"{TVTROPES_BASE_URL}{URL_SEP}{category}{URL_SEP}{movie}"
            try:
                # Fetch full page
                soup = fetch_page(url)
                # Process soup here
                movie_tropes = extract_trope_names(soup, url)
                tropes[movie] = movie_tropes
                found = True
                break  # Stop checking further categories
            except requests.exceptions.RequestException as e:
                continue  # Try next category
        if not found:
            print(f"No valid URL found for {movie}")
    
    return tropes

def main():
    file = sys.argv[1]
    if not file:
        print("Usage: python tvtropes_scraper.py <url> [<url> ...]")
        sys.exit(1)

    print(file)
    lb_data = pd.read_csv(file, sep = ",")
    movie_titles = lb_data["URLSafeNames"]

    movie_titles = movie_titles[:5]

    print(f"n. movies {len(movie_titles)}")
    tropes = get_tropes_for_movies(movie_titles)
    print(f"n. tropes found: {len(tropes)}")

    #trope_stats = pd.DataFrame(columns=["tropes","n_occurences","all_ratings"])

    for movie, m_tropes in tropes.items():
        print(movie, m_tropes)
        #i_data = list(movie_titles).index(movie)
        #rating = lb_data.loc[i_data, "Rating"]
    
    # TODO: 1. create list with ratings and list with lists of tropes
    # 2. loop over those lists and create a new dictionairy with key = trope, value = (number of occurences, cumulative rating)


if __name__ == "__main__":
    main()

