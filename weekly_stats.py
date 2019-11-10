from http_request import simple_get

import argparse
import json
import re
import os

from bs4 import BeautifulSoup

def stats_scraper(url, mode="weekly"):
    
    if mode == "weekly":
        keys = ['score', 'scored by', 'ranked', 'popularity', 'members', 'favorites', 
                'watching', 'completed', 'onhold', 'dropped', 'plan to watch', 'total']
    elif mode == "season":
        keys = ['english', 'japanese', 'type', 'episodes', 'status', 'aired', 'premiered', 
                'broadcast', 'producers', 'licensors', 'studios', 'source', 'genres', 
                'duration', 'rating']
        
    stats = dict.fromkeys(keys)
    
    # Get stats page from url
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')

    info = html.find_all("span", {"class": "dark_text"})
    
    # Populate stats dictionary
    for i in info:
        key = re.sub(r'[^\w\s]','',(i.text).lower())
        if key in keys:
            stats[key] = (i.next_sibling).strip()
    
    if html.find("span", {"itemprop": "ratingValue"}) != None:
        stats["score"] = (html.find("span", {"itemprop": "ratingValue"})).text
    if html.find("span", {"itemprop": "ratingCount"}) != None:
        stats["scored by"] = (html.find("span", {"itemprop": "ratingCount"})).text
   
    return stats


def forum_scraper(url):
    
    keys = ["votes", "replies"]
    stats = dict.fromkeys(keys)
    
    # Get forum topic from url
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    
    topic = html.find("tr", {"id": "topicRow1"})
        
    if topic == None:
        return stats
    
    stats["replies"] = topic.find("td", {"align": "center", "class": "forum_boardrow2", "width": "75"}).text
    
    forum_query = (topic.find("small")).find_previous('a')['href']
    print(url)
    print(forum_query)
    # Get episode discussion
    raw_html = simple_get("https://myanimelist.net/" + forum_query + "&pollresults=1")
    html = BeautifulSoup(raw_html, 'html.parser')
    
    tables = html.find_all("tr")
    
    stats["votes"] = [0] * 5
    for idx, t in enumerate(tables):
        stats["votes"][idx] = t.find("td", {"align": "center"}).text   
        if idx == 4: break
    
    return stats

def get_stats(id):
    with open(os.path.join("output", "seasonal_list.json")) as json_file:
        data = json.load(json_file)
        
        for category in data:
            for idx, anime in enumerate(data[category]):
                if id == list(anime)[0]:
                    a = list(anime.values())[0]
                    
                    stats_link = a["link"] + "/stats"
                    stats = stats_scraper(stats_link, mode="weekly")  # mode="weekly" or mode="seasonal"
                    data[category][idx][id]["stats"]["user_stats"].append(stats)
                    print(data[category][idx][id]["stats"]["user_stats"])
                    
                    forum_link = a["link"] + "/forum?topic=episode"
                    epi_stats = forum_scraper(forum_link)
                    data[category][idx][id]["stats"]["episode_score"].append(epi_stats)
                    print(data[category][idx][id]["stats"]["episode_score"])
                    
                    break
                    
    with open(os.path.join("output", "seasonal_list.json"), 'w') as outfile:
        json.dump(data, outfile, indent=4)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--id", help="anime id")

    args = parser.parse_args()
    
    get_stats(args.id)

   