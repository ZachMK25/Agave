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
    
    match = html_pattern.findall(str(soup))
    
    if match:
        print(True)
        print("MATCHED")
        description = match[0]
    else:
        print("NO MATCH\n")


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

    # added a txt to store all the ignored domains, 
    # may want to migrate to a DB or another method for doing this in the future
    
    with open("./excludedDomains.txt","r") as file:
        excluded_domains = set(line.strip() for line in file)

    if not excluded_domains:
        return ("missing excludedDomains.txt")

    sponsor_links = []

    for link in links:
        domain = tldextract.extract(link).domain
            
        if not domain in excluded_domains:
            sponsor_links.append(link)

    if printing:       
        print("sponsor links:\n",sponsor_links,"\n\n")
    
    return {
        "sponsor_links":sponsor_links,
        "affiliate_links":affiliate_links,
        "shortened_links":shortened_links
    }

sys.modules[__name__] = scrape_description