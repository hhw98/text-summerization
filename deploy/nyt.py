#nyt.py
from secrete import *
import requests
from bs4 import BeautifulSoup

# gets stories from a particular section of NY times
def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key':nyt_key}
    #a = requests.get(baseurl, params)
    #print(extendedurl)
    return requests.get(extendedurl, params).json()

def get_headlines(nyt_results_dict):
    results = nyt_results_dict['results']
    headlines = []
    for r in results:
        headlines.append(r['url'])
    return headlines

def get_article(word = "science"):
    story_list_json = get_stories(word)
    headlines = get_headlines(story_list_json)
    html = requests.get(headlines[0]).text
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find("section", {"name":"articleBody"})
    return t.text

