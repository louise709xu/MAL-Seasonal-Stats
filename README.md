## MAL Seasonal Stats

### seasonals.py
Creates a json file (seasonal_list.json) with all currently airing anime and their scheduled release

Usage:    
`python seasonals.py`

Output Format:
```
{
    "TV (New)": [
        {
            "id": "38408",
            "title": "Boku no Hero Academia 4th Season",
            "link": "https://myanimelist.net/anime/38408/Boku_no_Hero_Academia_4th_Season",
            "schedule": "Oct 12, 2019, 17:30 (JST)"
        }
    ]
}
```


### episode_scores.py
Creates a csv file (episode_stats.csv) with episode scores from each anime in seasonal_list.json. Due to the finicky nature of http requests, an additional json file (seasonal_list_error.json) is created that contains all the anime where the stat gathering was unsuccessful.

Usage:    
`python episode_scores.py`    
or     
`python episode_scores.py seasonal_list_error.json`

Output Format:
```
,5,4,3,2,1,Score
Dr. Stone,512,53,19,7,4,4.784873949579832
```
