from datetime import datetime, timedelta
import pytz
import json
import os

cron_jobs = []

with open(os.path.join("output", "seasonal_list.json")) as json_file:
    data = json.load(json_file)
    for category in data:
        for anime in data[category]:
            a = list(anime.values())[0]
            anime_id = list(anime)[0]
            
            # Date format: Oct 12, 2019, 17:30 (JST)
            try:
                date = a["schedule"].replace("JST", "+0900")
                date_time_obj = datetime.strptime(date, "%b %d, %Y, %H:%M (%z)")
                date_time_obj = date_time_obj + timedelta(hours=-1)
            except:
                try:
                    date = a["schedule"] + ", 00:00 (+0900)"
                    date_time_obj = datetime.strptime(date, "%b %d, %Y, %H:%M (%z)")
                    date_time_obj = date_time_obj + timedelta(hours=-1)
                except:
                    print("Invalid schedule: ", anime)
                    
            cron_schedule = date_time_obj.astimezone(pytz.utc).strftime("%M %H * * %a")
            cron_job = cron_schedule + " /usr/bin/python /home/pi/MAL-Seasonal-Stats/weekly_stats.py " + anime_id
            cron_jobs.append(cron_job)

with open(os.path.join("output", 'cron.txt'), 'w') as file:
    for c in cron_jobs:
        file.write('%s\n' % c)
        
print("\nComplete!")
