from bs4 import BeautifulSoup
import requests

import re

# NEED TO FOLLOW YOUTUBE'S ROBOTS.TXT

trending_url = "https://www.youtube.com/feed/trending"

html = requests.get(trending_url).content

soup = BeautifulSoup(html, features="html.parser")

# <yt-formatted-string id="description-text" class="style-scope ytd-video-renderer">

# thumbnail_links = soup.find_all('a')
# print(soup.html)
html_pattern = re.compile('"videoId":"(.*?)"')
all_video_ids = html_pattern.findall(str(soup))


# for link in thumbnail_links:
#     print(link)
#     print(link.get('href'))