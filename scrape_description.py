from bs4 import BeautifulSoup
import requests
import re
import tldextract
import os.path
import sys

def scrape_description(video_identifier):

    # We can cut the whole cache thing once we refine the extraction, 
    # I just done wanna get blocked by YouTube when I am making so many requests

    FORCE_RENEW_CACHE = True
    # check if the cache file has been used before and has something in it.
    # using this for now to not blacklist us from youtube requests. need to figure out something more permanent in the future
    cache_exists = os.path.isfile("cache.txt") and os.stat("cache.txt").st_size != 0
    
        
    youtube_url = "https://youtube.com/watch?v="+video_identifier
    
    # maybe some url validation here
    
    
    # need to avoid rate limiting from youtube
    if not cache_exists or FORCE_RENEW_CACHE:
        # https://stackoverflow.com/questions/72354649/how-to-scrape-youtube-video-description-with-beautiful-soup

        soup = BeautifulSoup(requests.get(youtube_url).content, features="html.parser")

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

    link_pattern = re.compile('https://[a-zA-Z0-9\-\?\/\.\?]*')

    links = link_pattern.findall(description)
    
    shortened_link_pattern = re.compile('https?:\/\/(?:bit\.ly|goo\.gl|ow\.ly|tinyurl\.com)\/\S+')
    shortened_links = shortened_link_pattern.findall(description)

    # affiliate link pattern
    affiliate_link_pattern = re.compile('https?:\/\/\S+\?(?:ref|affiliate_id|promo)=\S+')
    affiliate_links = affiliate_link_pattern.findall(description)

    print("all links found in description:\n",links,"\n")
    print("found the following shortened links\n",shortened_links,"\n")
    print("found the following affiliate links\n",affiliate_links,"\n")

    # throw out links to socials, add more as needed
    # eventually want a more thorough way of validating whether a link would be to a sponsor

    common_socials = ["x", "instagram", "bsky", "youtube", "facebook"]

    sponsor_links = []

    for link in links:
        domain = tldextract.extract(link).domain
            
        if not domain in common_socials:
            sponsor_links.append(link)
            
    print("sponsor links:\n",sponsor_links,"\n\n")
    
    return {
        "sponsor_links":sponsor_links,
        "affiliate_links":affiliate_links,
        "shortened_links":shortened_links
    }

sys.modules[__name__] = scrape_description