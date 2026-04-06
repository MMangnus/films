import requests
import json
import re
import scipy.stats
import numpy as np
from bs4 import BeautifulSoup
import sys
import matplotlib.pyplot as plt
import pandas as pd

def load_data(file_path: str) -> tuple[pd.DataFrame, pd.Series]:
    """Load CSV data and extract movie titles."""
    print("Loading data")
    lb_data = pd.read_csv(file_path, sep=",")
    return lb_data

# def get_letterboxd_data(url):
#     '''Scrape data from general letterboxd page'''
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.text, "html.parser")
#     script = soup.find("script", type="application/ld+json")
#     if not script:
#         return None
#     cleaned = re.sub(r'/\*.*?\*/', '', script.string, flags=re.DOTALL).strip()
#     data = json.loads(cleaned)
#     return {
#         "title": data.get("name"),
#         "year": data.get("releasedEvent", [{}])[0].get("startDate"),
#         "rating": data.get("aggregateRating", {}).get("ratingValue"),
#         "genres": data.get("genre"),
#         "director": [d.get("name") for d in data.get("director", [])],
#         "actors": [d.get("name") for d in data.get("actors", [])],
#     }

def main():
    # Validate command line argument
    if len(sys.argv) < 2:
        print("Usage: python analyze_ratings.py input_file.csv")
        sys.exit(1)
    file = sys.argv[1]

    # Load data
    lb_data = load_data(file)

    #lb_data = lb_data[:50]   

    # # Plot movie ratings
    # fig, ax = plt.subplots(nrows = 1,ncols = 1, figsize = (5, 4), dpi = 150)
    # plt.hist(lb_data['Year'], rwidth=0.8, color = '#00E054')
    # ax.set_title('Release year from all movies')
    # ax.set_ylabel('Frequency')
    # ax.set_xlabel("Year")   
    # ax.set_xlim(1925,2025)
    # plt.savefig("year_hist.svg")      


    # # Plot movie ratings
    # fig, ax = plt.subplots(nrows = 1,ncols = 1, figsize = (5, 4), dpi = 150)
    # plt.bar(genre_df['genre'], genre_df['count'], color = '#FF8000')    
    # ax.set_title('Genres Watched')
    # ax.set_ylabel('Frequency')
    # ax.set_xlabel("Genre")   
    # #ax.set_xlim(1925,2025)
    # plt.savefig("genre_bar.svg")     
    # # Get actor stats
    # genre_stats = {}
    # for movie in lb_data['Name']:
    #     #print(movie)
    #     genres = lb_data[lb_data['Name'] == movie]['Genres']
    #     my_rating = lb_data[lb_data['Name'] == movie]['Rating'].item()
    #     avg_rating = lb_data[lb_data['Name'] == movie]['Avg Rating'].item()
    #     genres = genres.to_list()
    #     genres_list = re.sub(r"[\[\]\'\ ]", '', genres[0]).split(',')
    #     genres_list = genres_list[:20]
    #     for genre in genres_list:
    #         if genre in genre_stats:
    #             genre_stats[genre][0] += 1
    #             genre_stats[genre][1] += my_rating
    #             genre_stats[genre][2] += avg_rating
    #             genre_stats[genre][3].append(movie)
    #         else:
    #             genre_stats[genre] = [1, my_rating, avg_rating, [movie]]
    
    # genre_df = pd.DataFrame([
    #     {'genre': genre, 
    #      'count': stats[0], 
    #      'my_rating_cumul': stats[1], 
    #      'avg_rating_cumul': stats[2],
    #      'movies_of_genre': stats[3]}
    #     for genre, stats in genre_stats.items()
    # ])
    # genre_df['my_rating'] = genre_df['my_rating_cumul'] / genre_df['count']
    # genre_df['avg_rating'] = genre_df['avg_rating_cumul'] / genre_df['count']
    # genre_df['diff_rating'] = genre_df['my_rating'] - genre_df['avg_rating']
    # genre_df = genre_df.drop(columns=['my_rating_cumul', 'avg_rating_cumul'])  
    # genre_df = genre_df[genre_df['genre'] != 'TVMovie']
    # #genre_df.to_csv('genre_stats.csv', index=False, float_format="%.2f")   

    # # Get actor stats
    # actor_stats = {}
    # for movie in lb_data['Name']:
    #     print(movie)
    #     actors = lb_data[lb_data['Name'] == movie]['Actors']
    #     my_rating = lb_data[lb_data['Name'] == movie]['Rating'].item()
    #     avg_rating = lb_data[lb_data['Name'] == movie]['Avg Rating'].item()
    #     actors = actors.to_list()
    #     actors_list = re.sub(r"[\[\]\'\ ]", '', actors[0]).split(',')
    #     actors_list = actors_list[:20]
    #     for actor in actors_list:
    #         if actor in actor_stats:
    #             actor_stats[actor][0] += 1
    #             actor_stats[actor][1] += my_rating
    #             actor_stats[actor][2] += avg_rating
    #             actor_stats[actor][3].append(movie)
    #         else:
    #             actor_stats[actor] = [1, my_rating, avg_rating, [movie]]
    
    # actors_df = pd.DataFrame([
    #     {'actor': actor, 
    #      'count': stats[0], 
    #      'my_rating_cumul': stats[1], 
    #      'avg_rating_cumul': stats[2],
    #      'movies_with_actor': stats[3]}
    #     for actor, stats in actor_stats.items()
    # ])
    # actors_df['my_rating'] = actors_df['my_rating_cumul'] / actors_df['count']
    # actors_df['avg_rating'] = actors_df['avg_rating_cumul'] / actors_df['count']
    # actors_df['diff_rating'] = actors_df['my_rating'] - actors_df['avg_rating']
    # actors_df = actors_df.drop(columns=['my_rating_cumul', 'avg_rating_cumul'])  
    #actors_df.to_csv('actor_stats.csv', index=False, float_format="%.2f")     
    # 
    # Get actor stats
    # director_stats = {}
    # for movie in lb_data['Name']:
    #     director = lb_data[lb_data['Name'] == movie]['Director']
    #     my_rating = lb_data[lb_data['Name'] == movie]['Rating'].item()
    #     avg_rating = lb_data[lb_data['Name'] == movie]['Avg Rating'].item()
    #     director = director.to_list()
    #     directors_list = re.sub(r"[\[\]\'\ ]", '', director[0]).split(',')
    #     #directors_list = directors_list[:20]
    #     for director in directors_list:
    #         if director in director_stats:
    #             director_stats[director][0] += 1
    #             director_stats[director][1] += my_rating
    #             director_stats[director][2] += avg_rating
    #             director_stats[director][3].append(movie)
    #         else:
    #             director_stats[director] = [1, my_rating, avg_rating, [movie]]
    
    # director_df = pd.DataFrame([
    #     {'director': director, 
    #      'count': stats[0], 
    #      'my_rating_cumul': stats[1], 
    #      'avg_rating_cumul': stats[2],
    #      'movies_from_director': stats[3]}
    #     for director, stats in director_stats.items()
    # ])
    # director_df['my_rating'] = director_df['my_rating_cumul'] / director_df['count']
    # director_df['avg_rating'] = director_df['avg_rating_cumul'] / director_df['count']
    # director_df['diff_rating'] = director_df['my_rating'] - director_df['avg_rating']
    # director_df = director_df.drop(columns=['my_rating_cumul', 'avg_rating_cumul'])  
    # director_df.to_csv('director_stats.csv', index=False, float_format="%.2f")             


if __name__ == "__main__":
    main()

    # # enrich csv file
    # avg_rating = []
    # genres = []
    # director = []
    # actors = []
    # loopcount = 0
    # for url in lb_data['Letterboxd URI']:
    #     print(loopcount)
    #     data_dict = get_letterboxd_data(url)
    #     avg_rating.append(data_dict['rating'])
    #     genres.append(data_dict['genres'])
    #     director.append(data_dict['director'])
    #     actors.append(data_dict['actors'])
    #     loopcount += 1
    # lb_data['Avg Rating'] = avg_rating
    # lb_data['Genres'] = genres
    # lb_data['Director'] = director
    # lb_data['Actors'] = actors

    # lb_data.to_csv("movie_ratings_enriched.csv", index=False, float_format="%.2f")

    # print(lb_data.head(10))