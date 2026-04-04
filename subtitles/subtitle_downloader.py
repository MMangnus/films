import requests
import time
import os
import zipfile

API_KEY = "your_subdl_api_key"
BASE = "https://api.subdl.com/api/v1/subtitles"

movies = [
    "Inception",
    "The Godfather",
    "Blade Runner",
    # ... add more titles here
]

os.makedirs("subtitles", exist_ok=True)


def safe_extract(zip_path, dest_folder):
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            # Only extract subtitle files
            if not member.lower().endswith(('.srt', '.ass', '.ssa', '.vtt')):
                continue
            # Prevent path traversal
            member_path = os.path.realpath(os.path.join(dest_folder, os.path.basename(member)))
            if not member_path.startswith(os.path.realpath(dest_folder)):
                continue  # skip suspicious paths
            with z.open(member) as src, open(member_path, 'wb') as dst:
                dst.write(src.read(10 * 1024 * 1024))  # cap at 10MB per file


for title in movies:
    safe_title = title.replace(" ", "_")
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
        "api_key": API_KEY,
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

    time.sleep(1)  # be polite to the API
