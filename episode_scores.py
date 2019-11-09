from http_request import simple_get

import json
import pandas as pd
import time
import re
import os
import argparse

from bs4 import BeautifulSoup

def get_episode_scores(anime_file="seasonal_list_episode.json"):
    ep_scores = dict()
    error_anime = {}
    
    with open(os.path.join("output", anime_file)) as json_file:
        data = json.load(json_file)
    
        for category in data:
            error_anime[category] = []
            
            # Scrap each seasonal's page for stats
            for anime in data[category]:
                # Try to scrape each page
                # May not work if too many requests at once
                try:
                    a = list(anime.values())[0]
                    url = a["link"] + "/forum?topic=episode"
    
                    # Get anime forum page
                    raw_html = simple_get(url)
                    html = BeautifulSoup(raw_html, 'html.parser')

                    topic = html.find("tr", {"id": "topicRow1"})
                    forum_query = (topic.find("small")).find_previous('a')['href']

                    # Get most recent episode discussion thread
                    raw_html = simple_get("https://myanimelist.net/" + forum_query + "&pollresults=1")
                    html = BeautifulSoup(raw_html, 'html.parser')

                    tables = html.find_all("tr")

                    # Populate scores dictionary
                    ep_scores[a["title"]] = [0] * 5
                    for idx, t in enumerate(tables):
                        ep_scores[a["title"]][idx] = t.find("td", {"align": "center"}).text   
                        if idx == 4: break
                # If scraping is unsuccessful, print out contents of dict
                except:
                    error_anime[category].append(anime)
                    print(anime)

                # Delay to prevent too many requests at once
                time.sleep(1) 

    # Convert dictionary to dataframe
    ep = pd.DataFrame.from_dict(ep_scores, orient='index', columns=['5', '4', '3', '2', '1'])
    ep = ep.replace(r'^\s*$', 0, regex=True)
    ep = ep.astype('int')

    # Add score column
    ep['score'] = (ep['5']*5 + ep['4']*4 + ep['3']*3 + ep['2']*2 + ep['1']*1) / ep.sum(axis=1)

    csv_filename = os.path.join("output", "episode_stats.csv")
    
    if os.path.exists(csv_filename):
        file_mode = 'a' # append if already exists
        include_header = False
    else:
        file_mode = 'w' # make a new file if not
        include_header = True

    # Export file to csv
    with open(csv_filename, file_mode) as f:
        ep.to_csv(f, header=include_header, newline='')
    
    with open(os.path.join("output", "seasonal_list_episode.json"), 'w') as outfile:
        json.dump(error_anime, outfile, indent=4)

if __name__ == "__main__":
    print("Getting episode scores...")
    get_episode_scores()
    print("\nComplete!")