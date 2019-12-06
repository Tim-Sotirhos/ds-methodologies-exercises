'''
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

# make original df and then create a copy
original_df = acquire.get_news_articles()
original_df

prepped_df = original_df.copy()

prepped_df.columns
prepped_df.drop(columns = 'Unnamed: 0', inplace = True)

# lowercase every column
prepped_df.author = prepped_df.author.str.lower()
prepped_df.category = prepped_df.category.str.lower()
prepped_df.content = prepped_df.content.str.lower()
prepped_df.published_date = prepped_df.published_date.str.lower()
prepped_df.title = prepped_df.title.str.lower()

# normalize unicode characters
def normalize(string):
    return unicodedata.normalize('NFKD', string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')

prepped_df.author = prepped_df.author.apply(normalize)
prepped_df.category = prepped_df.category.apply(normalize)
prepped_df.content = prepped_df.content.apply(normalize)
prepped_df.published_date = prepped_df.published_date.apply(normalize)
prepped_df.title = prepped_df.title.apply(normalize)

# replace anything that is not a letter, number, whitespace or a single quote.

def remove_special_characters(string):
    return re.sub(r"[^a-z0-9'\s]", '', string)

prepped_df.author = prepped_df.author.apply(remove_special_characters)
prepped_df.category = prepped_df.category.apply(remove_special_characters)
prepped_df.content = prepped_df.content.apply(remove_special_characters)
prepped_df.title = prepped_df.title.apply(remove_special_characters)

def basic_clean():


# tokenization
'''
# Solution

import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import acquire

def basic_clean(string):
    """
    Lowercase the string
    Normalize unicode characters
    Replace anything that is not a letter, number, whitespace or a single quote.
    """
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # remove anything not a space character, an apostrophy, letter, or number
    string = re.sub(r"[^a-z0-9'\s]", '', string)

    # convert newlins and tabs to a single space
    string = re.sub(r'[\r|\n|\r\n]+', ' ', string)
    string = string.strip()
    return string

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string, return_str=True)

def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string_of_stems = ' '.join(stems)
    return string_of_stems

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string_of_lemmas = ' '.join(lemmas)
    return string_of_lemmas


def remove_stopwords(string, extra_words=[], exclude_words=[]):
    # Tokenize the string
    string = tokenize(string)

    words = string.split()
    stopword_list = stopwords.words('english')

    # remove the excluded words from the stopword list
    stopword_list = set(stopword_list) - set(exclude_words)

    # add in the user specified extra words
    stopword_list = stopword_list.union(set(extra_words))

    filtered_words = [w for w in words if w not in stopword_list]
    final_string = " ".join(filtered_words)
    return final_string

def prep_articles(df):
    df["original"] = df.body
    df["stemmed"] = df.body.apply(basic_clean).apply(stem)
    df["lemmatized"] = df.body.apply(basic_clean).apply(lemmatize)
    df["clean"] = df.body.apply(basic_clean).apply(remove_stopwords)
    df.drop(columns=["body"], inplace=True)
    return df

def prep_blog_posts():
    df = acquire.get_blog_posts()
    return prep_articles(df)

def prep_news_articles():
    df = acquire.get_news_articles()
    return prep_articles(df)

def prep_corpus():
    blog_df = prep_blog_posts()
    blog_df["source"] = "Codeup Blog"

    news_df = prep_news_articles()
    news_df["source"] = "InShorts News"

    return blog_df, news_df