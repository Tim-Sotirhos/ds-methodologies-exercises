# Data Acquisition Exercises - Time Series

import json
import requests
import pandas as pd

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
