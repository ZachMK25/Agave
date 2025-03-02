from bs4 import BeautifulSoup
import requests
import re
import tldextract
import os.path
import sys

def scrape_description(video_identifier, printing=False):
        
    youtube_url = "https://youtube.com/watch?v="+video_identifier
    
    # maybe some url validation here
    

    # https://stackoverflow.com/questions/72354649/how-to-scrape-youtube-video-description-with-beautiful-soup

    soup = BeautifulSoup(requests.get(youtube_url).content, features="html.parser")

    html_pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')

    description = html_pattern.findall(str(soup))[0].replace('\\n','\n')

    # finding links within description

    link_pattern = re.compile('https://[a-zA-Z0-9\-\?\/\.\?]*')

    links = link_pattern.findall(description)
    
    shortened_link_pattern = re.compile('https?:\/\/(?:bit\.ly|goo\.gl|ow\.ly|tinyurl\.com)\/\S+')
    shortened_links = shortened_link_pattern.findall(description)

    # affiliate link pattern
    affiliate_link_pattern = re.compile('https?:\/\/\S+\?(?:ref|affiliate_id|promo)=\S+')
    affiliate_links = affiliate_link_pattern.findall(description)

    if printing:
        print("*** URL", youtube_url)
        print("extracted description", description)
        print("all links found in description:\n",links,"\n")
        print("found the following shortened links\n",shortened_links,"\n")
        print("found the following affiliate links\n",affiliate_links,"\n")

    # throw out links to socials, add more as needed
    # eventually want a more thorough way of validating whether a link would be to a sponsor

    common_socials = ["x", "instagram", "bsky", "youtube", "facebook", "discord", "tiktok"]

    sponsor_links = []

    for link in links:
        domain = tldextract.extract(link).domain
            
        if not domain in common_socials:
            sponsor_links.append(link)

    if printing:       
        print("sponsor links:\n",sponsor_links,"\n\n")
    
    return {
        "sponsor_links":sponsor_links,
        "affiliate_links":affiliate_links,
        "shortened_links":shortened_links
    }

sys.modules[__name__] = scrape_description