"""
TV Tropes and Movie Ratings Analysis
=====================================

Analyzes the relationship between movie tropes (from TV Tropes) and their ratings 
(from Letterboxd data). Fetches trope data for movies, computes statistics about 
trope frequency and average ratings, and generates visualizations. 

The input .csv file is an adapted version of the file that can be exported from
Letterboxd (Account Settings --> Data tab). This raw file should be enriched with
a column that converts the default Name column into a column that contains movie 
titles that comply with the URLs on the tv tropes website.

Usage:
    python analyze_tropes.py <input_file.csv>

Example:
    python analyze_tropes.py ../movie_ratings.csv

Input:
    - CSV file with columns: 'URLSafeNames' (movie names for TV Tropes URLs) and 'Rating' (ratings)

Output:
    - movie_ratings.svg: Histogram of all movie ratings from the input file
    - trope_stats.svg: Histograms showing trope frequency and average ratings
    - trope_ratings.csv: Trope statistics (name, count, average rating, associated movies)

Dependencies:
    = tvtropes_scraper.py
    - pandas
    - matplotlib
    - requests
    - beautifulsoup4
    - cloudscraper
"""

import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
from tvtropes_scraper import fetch_page, extract_trope_names

CATEGORIES_TVTROPES = ["Film", "WesternAnimation", "Series", "Anime", "Manga","Animation"]
TVTROPES_BASE_URL = "https://tvtropes.org/pmwiki/pmwiki.php"
URL_SEP = "/"

def get_tropes_for_movies(movie_titles: list[str]) -> dict[str, list[str]]:
    'Read urls from column of csv, fetch page, and extract trope names for each movie.'

    print("Get tropes from TV Tropes URLs")
    tropes = {}
    for movie in movie_titles:
        found = False
        for category in CATEGORIES_TVTROPES:
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

def load_data(file_path: str) -> tuple[pd.DataFrame, pd.Series]:
    """Load CSV data and extract movie titles."""
    print("Loading data")
    lb_data = pd.read_csv(file_path, sep=",")
    movie_titles = lb_data["URLSafeNames"]
    return lb_data, movie_titles

def compute_trope_stats(tropes_per_movie, lb_data: pd.DataFrame) -> dict:
    """Compute trope statistics from movie tropes and ratings."""
    trope_stats = {}
    for movie, m_tropes in tropes_per_movie:
        movie_rating = lb_data[lb_data['URLSafeNames'] == movie]['Rating']
        if len(movie_rating) == 1:
            movie_rating = movie_rating.item()
        else:
            raise Exception(f"Found more than one row with the movie name {movie} in the .csv file")
        for trope in m_tropes:
            if trope in trope_stats:
                trope_stats[trope][0] += 1
                trope_stats[trope][1] += movie_rating
                trope_stats[trope][2].append(movie)
            else:
                trope_stats[trope] = [1, movie_rating, [movie]]
    return trope_stats

def create_stats_dataframe(trope_stats: dict) -> pd.DataFrame:
    """Create and process the stats DataFrame."""
    stats_df = pd.DataFrame([
        {'trope': trope, 
         'count': stats[0], 
         'cumulative_rating': stats[1], 
         'movies_with_trope': stats[2]}
        for trope, stats in trope_stats.items()
    ])
    stats_df['avg_rating'] = stats_df['cumulative_rating'] / stats_df['count']
    stats_df = stats_df.drop(columns=['cumulative_rating'])
    return stats_df

def save_results(stats_df: pd.DataFrame, output_file: str = "trope_ratings.csv"):
    """Save the results to a CSV file."""
    stats_df.to_csv(output_file, index=False, float_format="%.2f")

def plot_stats(stats_df: pd.DataFrame, fig_title: str = "trope_stats.svg"):
    """Plots histograms of counts and ratings of tropes"""    
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize = (10, 4), dpi = 100)
    axs[0].hist(stats_df['count'], rwidth=0.8, color = '#00E054')
    axs[0].set_title('Number of movies a trope has appeared in')
    axs[0].set_xlabel("Number of movies that have the trope")
    axs[0].set_ylabel("Frequency")
    axs[1].hist(stats_df['avg_rating'], rwidth=0.8, color = '#40BCF4') 
    axs[1].set_title('Average trope rating')
    axs[1].set_xlim(0,5)
    axs[1].set_xlabel("Trope rating (0.5 to 5)")
    axs[1].set_ylabel("Frequency")
    fig.tight_layout()
    plt.savefig(fig_title)

def main():
    # Validate command line argument
    if len(sys.argv) < 2:
        print("Usage: python analyze_ratings.py input_file.csv")
        sys.exit(1)
    file = sys.argv[1]

    # Load data
    lb_data, movie_titles = load_data(file)

    # Plot movie ratings
    #plot_movie_ratings(lb_data, fig_title = "movie_ratings.svg")

    # Fetch tropes
    tropes = get_tropes_for_movies(movie_titles)
    tropes_per_movie = tropes.items()
    print(f"number of movie pages found on tv tropes: {len(tropes_per_movie)}")

    # Compute stats
    trope_stats = compute_trope_stats(tropes_per_movie, lb_data)

    # Create DataFrame
    stats_df = create_stats_dataframe(trope_stats)
    stats_df_mincount5 = stats_df[stats_df['count'] > 4]

    # Make plots
    plot_stats(stats_df, fig_title = "trope_stats.svg")
    plot_stats(stats_df_mincount5, fig_title = "trope_stats_countmin5.svg")

    # Save results for all tropes and trope that occur at least 5 times
    save_results(stats_df, "trope_ratings.csv")
    save_results(stats_df_mincount5, "trope_ratings_mincount5.csv")

if __name__ == "__main__":
    main()
