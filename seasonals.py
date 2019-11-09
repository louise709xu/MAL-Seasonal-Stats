from http_request import simple_get

import json
import os

from bs4 import BeautifulSoup

def get_seasonal_anime():
    # Add or remove any of these categories from the list:
    # ["TV (New)", "TV (Continuing)", "ONA", "OVA", "Movie", "Special"]
    # By default, only "TV (New)" and "ONA" are included
    valid_categories = ["TV (New)", "ONA"]

    seasonal_url = "https://myanimelist.net/anime/season"

    anime = {}

    # Get html under each category from url
    raw_html = simple_get(seasonal_url)
    html = BeautifulSoup(raw_html, 'html.parser')

    categories = html.find_all("div", {"class": "js-seasonal-anime-list"})

    # Loop through each category
    for c in categories:
        category = c.find("div", {"class": "anime-header"}).text

        # Skip categories not found in valid_categories
        if category not in valid_categories:
            continue

        anime[category] = []

        ids = c.find_all("div", {"class": "genres js-genre"})
        titles = c.find_all("a", {"class": "link-title"})
        schedules = c.find_all("span", {"class": "remain-time"})

        for idx, id_ in enumerate(ids):
            anime[category].append(
            {
                id_.get('id') : {
                    "title" : (titles[idx].text).strip(),
                    "link" : titles[idx]['href'],
                    "schedule" : (schedules[idx].text).strip(),
                    "stats" : {
                        "episode_score" : [],
                        "user_stats" : []
                    }
                }
            })

    with open(os.path.join("output", "seasonal_list.json"), 'w') as outfile:
        json.dump(anime, outfile, indent=4)
        
    with open(os.path.join("output", "seasonal_list_episode.json"), 'w') as outfile:
        json.dump(anime, outfile, indent=4)

if __name__ == "__main__":
    print("Gathering seasonal anime...")
    get_seasonal_anime()
    print("\nComplete!")