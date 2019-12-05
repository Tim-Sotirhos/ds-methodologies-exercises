from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
import json
from os import path

def make_dictionary_from_article(url):
    # make the request to the url variable
    headers = {'User-Agent': 'Codeup Bayes Data Science'} # codeup.com doesn't like our default user-agent
    response = get(url, headers=headers)

    # make a "soup" variable
    soup = BeautifulSoup(response.content, 'html.parser')

    # isolate the title of the article, store it as a string called "title"
    title = soup.select('#mk-page-introduce')
    title = title[0].text

    # isolate the body text of the article and name the variable "body"
    body = soup.find('div', class_ = 'mk-single-content')
    body = article.text

    return {
        "title": title,
        "body": body
    }

def get_blog_articles():
    # if we already have the data, read it locally
    if path.exists('Codeup_blog_articles.json'):
        with open('Codeup_blog_articles.json') as f:
            return json.load(f)
            
    urls = [
        "https://codeup.com/codeups-data-science-career-accelerator-is-here/",
        "https://codeup.com/data-science-myths/",
        "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/",
        "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/",
        #"https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/",
    ]
    
    output = []

    for url in urls:
        print('processing',url)
        output.append(make_dictionary_from_article(url))
        
    # save it for next time
    with open('Codeup_blog_articles.json', 'w') as f:
        json.dump(output, f)

    return output

articles = get_blog_articles()
articles
