## MAL Seasonal Stats

### seasonals.py
Creates two identical json files (seasonal_list.json and seasonal_list_episode.json) with all currently airing anime and their scheduled release

Usage:    
`python seasonals.py`

Output Format:
```
{
    "TV (New)": [
        {
            "39940": {
                "title": "Shokugeki no Souma: Shin no Sara",
                "link": "https://myanimelist.net/anime/39940/Shokugeki_no_Souma__Shin_no_Sara",
                "schedule": "Oct 12, 2019, 00:30 (JST)",
                "stats": {
                    "episode_score": [],
                    "user_stats": []
                }
            }
        },
    ]
}
```


### episode_scores.py
Creates a csv file (episode_stats.csv) with episode scores from each anime in seasonal_list.json. Due to the finicky nature of http requests, the duplicate json file (seasonal_list_episode.json) is rewritten with all the anime where the stat gathering was unsuccessful.

Usage:    
`python episode_scores.py`    

Output Format:
```
,5,4,3,2,1,Score
Dr. Stone,512,53,19,7,4,4.784873949579832
```


### generate_cron.py
Generates cron jobs for each anime

Usage:
`python generate_cron.py`

Output Format:
```
30 07 * * Sat /usr/bin/python /home/pi/MAL-Seasonal-Stats/weekly_stats.py 38408
```


### weekly_stats.py
Script that is run through cron automatically each week. Adds episode scores and user stats to seasonal_list.json

Usage:
`python weekly_stats.py [anime_id]`

Output Format:
```
{
    "TV (New)": [
        {
            "39940": {
                "title": "Shokugeki no Souma: Shin no Sara",
                "link": "https://myanimelist.net/anime/39940/Shokugeki_no_Souma__Shin_no_Sara",
                "schedule": "Oct 12, 2019, 00:30 (JST)",
                "stats": {
                    "episode_score": [
                        {
                            "votes": [
                                "59",
                                "22",
                                "8",
                                "2",
                                "2"
                            ],
                            "replies": "34"
                        }
                    ],
                    "user_stats": [
                        {
                            "score": "8.05",
                            "scored by": "14,138",
                            "ranked": "#504",
                            "popularity": "#850",
                            "members": "130,433",
                            "favorites": "636",
                            "watching": "69,516",
                            "completed": "5",
                            "onhold": "879",
                            "dropped": "575",
                            "plan to watch": "59,458",
                            "total": "130,433"
                        }
                    ]
                }
            }
        },
    ]
}
```    