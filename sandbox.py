from bs4 import BeautifulSoup
import requests
import re
import tldextract
import os.path

# check if the cache file has been used before and has something in it.
# using this for now to not blacklist us from youtube requests. need to figure out something more permanent in the future
cache_exists = os.path.isfile("cache.txt") and os.stat("cache.txt").st_size != 0

# need to avoid rate limiting from youtube
if not cache_exists:
    # https://stackoverflow.com/questions/72354649/how-to-scrape-youtube-video-description-with-beautiful-soup

    soup = BeautifulSoup(requests.get('https://www.youtube.com/watch?v=kfseJYyCz44').content, features="html.parser")

    html_pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')

    description = html_pattern.findall(str(soup))[0].replace('\\n','\n')

    print(description)

    cache_file = open("cache.txt", "w")

    cache_file.write(description)
    
    cache_file.close()
    
else: 
    cache_file = open("cache.txt", "r")
    description = cache_file.read()
    cache_file.close()

# finding links within description

link_pattern = re.compile('https://[a-zA-Z\?\/\.]*')

links = link_pattern.findall(description)

print("all links found in description:\n",links,"\n")

# throw out links to socials, add more as needed
# eventually want a more thorough way of validating whether a link would be to a sponsor

common_socials = ["x", "instagram", "bsky", "youtube", "facebook"]

sponsor_links = []

for link in links:
    domain = tldextract.extract(link).domain
        
    if not domain in common_socials:
        sponsor_links.append(link)
        
print("sponsor links:\n",sponsor_links,"\n\n")