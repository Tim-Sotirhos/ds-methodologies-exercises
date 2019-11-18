# Data Acquisition Exercises - Time Series

import json
import requests
import pandas as pd
from os import path


# 1. Create a dataframe named items that has all of the data for items.

# We will use the get function from requests and pass it a url:
url = 'https://python.zach.lol'
response = requests.get(url)

# .ok: a boolean that indicates that the response was successful (the server sent back a 200 response code)
# status code 200 = ok
response.ok

# .status_code: a number indicating the HTTP response status code
response.status_code

# .text: the raw response text
response.text

# Above we see that the repsonse we got back contains a JSON object (we could also verify this by visiting the URL in a web browser).
# Since the response is JSON, we can use the .json method on the response object to get a data structure we can work with.

data = response.json()
print(type(data))
data

#This API provides some documentation, so let's make a request so that we can take a look at it.

response = requests.get(url + '/documentation')

print(response.json()['payload'])

# Based on this, let's take a look at the items. We'll make our request, and explore the shape of the response that we get back.

response = requests.get('https://python.zach.lol/api/v1/items')

data = response.json()

data.keys()

data['payload'].keys()

# Here the response has some built-in properties that tell us how to get to subsequent pages.

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])

data['payload']['items'][:]

# We can turn this data into a pandas dataframe:

items = pd.DataFrame(data['payload']['items'])
items.head()

# Now that we've gotten the data from the first page, we can extract the data from the next page,

response = requests.get(url + data['payload']['next_page'])
data = response.json()

# Here the response has some built-in properties that tell us how to get to subsequent pages.

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])

# Add the next page onto the dataframe:

items = pd.concat([items, pd.DataFrame(data['payload']['items'])]).reset_index()

# Now that we've gotten the data from the second page, we can extract the data from the next page,

response = requests.get(url + data['payload']['next_page'])
data = response.json()

# Here the response has some built-in properties that tell us how to get to subsequent pages.

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])

# Add the next page onto the dataframe:

items = pd.concat([items, pd.DataFrame(data['payload']['items'])]).reset_index()

items.shape

# 2. Create a dataframe named stores that has all of the data for stores.

response = requests.get('https://python.zach.lol/api/v1/stores')

data = response.json()

data.keys()

data['payload'].keys()

# Here the response has some built-in properties that tell us how to get to subsequent pages.

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])

data['payload']['stores'][:]

# We can turn this data into a pandas dataframe:

stores = pd.DataFrame(data['payload']['stores'])
stores

stores.shape

# 3. Extract the data for sales. There are a lot of pages of data here, so your code will need to be a little more complex. 
# Your code should continue fetching data from the next page until all of the data is extracted.

response = requests.get('https://python.zach.lol/api/v1/sales')

data = response.json()

data.keys()

data['payload'].keys()

# Here the response has some built-in properties that tell us how to get to subsequent pages.

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])

data['payload']['sales'][:]

# We can turn this data into a pandas dataframe:

sales = pd.DataFrame(data['payload']['sales'])

sales.head()

sales.shape

## Solution set of functions:

BASE_URL = 'https://python.zach.lol'
API_BASE = BASE_URL + '/api/v1'

# Get store data

def get_store_data_from_api():
    url = API_BASE + '/stores'
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data['payload']['stores'])


# Get items data

def get_item_data_from_api():
    url = API_BASE + '/items'
    response = requests.get(url)
    data = response.json()

    stores = data['payload']['items']

    while data['payload']['next_page'] is not None:
        print('Fetching page {} of {}'.format(data['payload']['page'] + 1, data['payload']['max_page']))
        url = BASE_URL + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        stores += data['payload']['items']

    return pd.DataFrame(stores)


# Get sales data

def get_sale_data_from_api():
    url = API_BASE + '/sales'
    response = requests.get(url)
    data = response.json()

    stores = data['payload']['sales']

    while data['payload']['next_page'] is not None:
        print('Fetching page {} of {}'.format(data['payload']['page'] + 1, data['payload']['max_page']))
        url = BASE_URL + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        stores += data['payload']['sales']

    return pd.DataFrame(stores)



# 4. Save the data in your files to local csv files so that it will be faster to access in the future.

def get_store_data(use_cache=True):
    if use_cache and path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    df = get_store_data_from_api()
    df.to_csv('stores.csv', index=False)
    return df


def get_item_data(use_cache=True):
    if use_cache and path.exists('items.csv'):
        return pd.read_csv('items.csv')
    df = get_item_data_from_api()
    df.to_csv('items.csv', index=False)
    return df


def get_sale_data(use_cache=True):
    if use_cache and path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    df = get_sale_data_from_api()
    df.to_csv('sales.csv', index=False)
    return df


# 5. Combine the data from your three separate dataframes into one large dataframe.

def get_all_data():
    sales = get_sale_data()
    items = get_item_data()
    stores = get_store_data()

    sales = sales.rename(columns={'item': 'item_id', 'store': 'store_id'})

    return sales.merge(items, on='item_id').merge(stores, on='store_id')

def get_all_the_data():
    sales = pd.read_csv('sales.csv')
    items = pd.read_csv('items.csv')
    stores = pd.read_csv('stores.csv')

    sales = sales.rename(columns={'item': 'item_id', 'store': 'store_id'})

    return sales.merge(items, on='item_id').merge(stores, on='store_id')


# 6. Acquire the Open Power Systems Data for Germany, which has been rapidly expanding its renewable energy production in recent years. The data set includes country-wide totals of electricity consumption, wind power production, and solar power production for 2006-2017. You can get the data here: https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv

def get_opsd_data(use_cache=True):
    if use_cache and path.exists('opsd.csv'):
        return pd.read_csv('opsd.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd.csv', index=False)
    return df


# 7. Make sure all the work that you have done above is reproducible. That is, you should put the code above into separate functions in the acquire.py file and be able to re-run the functions and get the same data.