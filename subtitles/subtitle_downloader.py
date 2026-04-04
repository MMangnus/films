import requests
import time
import re
import os
import pandas as pd
import zipfile

FILE_API_KEY = "api_key_margot.txt"
BASE = "https://api.subdl.com/api/v1/subtitles"

def get_api_key(file: str) -> str:
    '''Reads API key from a text file'''
    f = open(file)
    api_key = f.readline()
    f.close()
    return api_key

def get_movie_titles(movie_titles_file: str) -> pd.DataFrame:
    '''Extracts movie names from .csv file in other folder'''
    lb_data = pd.read_csv(movie_titles_file, sep=",")
    return lb_data['Name']
    

def safe_extract(zip_path, dest_folder):
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            # Only extract subtitle files
            if not member.lower().endswith(('.srt', '.ass', '.ssa', '.vtt')):
                continue
            # Exclude subtitles for the deaf/hard-of-hearing
            if re.search("SDH", member):
                continue
            # Prevent path traversal
            member_path = os.path.realpath(os.path.join(dest_folder, os.path.basename(member)))
            if not member_path.startswith(os.path.realpath(dest_folder)):
                continue  # skip suspicious paths
            with z.open(member) as src, open(member_path, 'wb') as dest:
                dest.write(src.read(10 * 1024 * 1024))  # cap at 10MB per file

def main():

    api_key = get_api_key(FILE_API_KEY)

    movies = get_movie_titles(movie_titles_file="movie_titles_subs.csv")

    movies = movies[:3]

    os.makedirs("subtitles", exist_ok=True)

    for title in movies:
        safe_title = re.sub(r"[/:&\[\]#!?,]", "", title).replace(" ", "_").replace("'", "")
        dest_folder = f"subtitles/{safe_title}"

        # Skip if already downloaded
        if os.path.isdir(dest_folder) and any(
            f.endswith(('.srt', '.ass', '.ssa', '.vtt'))
            for f in os.listdir(dest_folder)
        ):
            print(f"⏭ Already exists: {title}")
            continue

        # Search
        r = requests.get(BASE, params={
            "api_key": api_key,
            "film_name": title,
            "languages": "EN",
            "subs_per_page": 1,
        })
        data = r.json()

        if data.get("subtitles"):
            sub = data["subtitles"][0]
            url = "https://dl.subdl.com" + sub["url"]

            zip_r = requests.get(url)
            zip_path = f"subtitles/{safe_title}.zip"

            with open(zip_path, "wb") as f:
                f.write(zip_r.content)

            os.makedirs(dest_folder, exist_ok=True)
            safe_extract(zip_path, dest_folder)
            os.remove(zip_path)  # clean up zip after extraction

            print(f"✓ {title}")
        else:
            print(f"✗ Not found: {title}")

        time.sleep(1.5)  # be polite to the API

if __name__ == "__main__":
    main()