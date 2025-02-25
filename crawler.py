from bs4 import BeautifulSoup
import requests
import re

import scrape_description # i know this should be an api request but for proof of concept, TODO FIXME

# NEED TO FOLLOW YOUTUBE'S ROBOTS.TXT

trending_url = "https://www.youtube.com/feed/trending"

html = requests.get(trending_url).content

soup = BeautifulSoup(html, features="html.parser")

# <yt-formatted-string id="description-text" class="style-scope ytd-video-renderer">

html_pattern = re.compile('"videoId":"(.*?)"')
all_video_ids = list(set(html_pattern.findall(str(soup))))

for video_id in all_video_ids:
    print(scrape_description(video_id)['sponsor_links'])
