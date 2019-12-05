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


def get_news_articles():
    filename = 'inshorts_news_articles.csv'

    # check for presence of the file or make a new request
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return make_new_request()

def get_articles_from_topic(url):
    headers = {'user-agent': 'Codeup Bayes Instructor Example'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    output = []

    articles = soup.select(".news-card")

    for article in articles: 
        title = article.select("[itemprop='headline']")[0].get_text()
        content = article.select("[itemprop='articleBody']")[0].get_text()
        author = article.select(".author")[0].get_text()
        published_date = article.select(".time")[0]["content"]
        category = response.url.split("/")[-1]

        article_data = {
            'title': title,
            'content': content,
            'category': category,
            'author': author,
            'published_date': published_date,
        }
        output.append(article_data)


    return output


def make_new_request():
    urls = [
        "https://inshorts.com/en/read/business",
        "https://inshorts.com/en/read/sports",
        "https://inshorts.com/en/read/technology",
        "https://inshorts.com/en/read/entertainment"
    ]

    output = []
    
    for url in urls:
        # We use .extend in order to make a flat output list.
        output.extend(get_articles_from_topic(url))

    print("stuff")
    print(output)
    df = pd.DataFrame(output)
    df.to_csv('inshorts_news_articles.csv') 

    return df

# Alternative solution for acquire Codeup_blog
'''
def get_blog_posts():
    filename = './codeup_blog_posts.csv'

    # check for presence of the file or make a new request
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return make_new_request()

def make_dictionary_from_article(url): 
    # Set header and user agent to increase likelihood that your request get the response you want
    headers = {'user-agent': 'Codeup Bayes Instructor Example'}

    # This is the actual HTTP GET request that python will send across the internet
    response = get(url, headers=headers)

    # response.text is a single string of all the html from that page
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.get_text()
    body = soup.select("div.mk-single-content.clearfix")[0].get_text()

    output = {}
    output["title"] = title
    output["body"] = body
    return output


def make_new_request():
    urls = [
        "https://codeup.com/codeups-data-science-career-accelerator-is-here/",
        "https://codeup.com/data-science-myths/",
        "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/",
        "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/",
        "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/",
    ]

    output = []
    
    for url in urls:
        article_dictionary = make_dictionary_from_article(url)
        output.append(article_dictionary)

    df = pd.DataFrame(output)
    df.to_csv('./codeup_blog_posts.csv') 

    return df
'''