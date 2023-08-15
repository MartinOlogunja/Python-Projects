#Import packages

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '11105560-0723-494c-96fd-9c1e23842ecf',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

#The rate limit in Jupyter notebook had to be changed using "jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10"
#This was done in the Anaconda Prompt Python Terminal


# Check the datatype that's been pulled
type(data)


#Import pandas in order to view and manipulate the dataframe
import pandas as pd

#This allows you to see all the columns
pd.set_option('display.max_columns', None)

#This allows you to see all the rows
pd.set_option('display.max_rows', None)


#This normalises the data and sets it to the dataframe
df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


#Creating a function that will request data from CMC and append to a dataframe. 
def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '11105560-0723-494c-96fd-9c1e23842ecf',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now', utc=True)
    df
    
    if not os.path.isfile(r'/Users/marti/Desktop/data_analyst_portfolio/python/CMC_API.csv'):
        df.to_csv(r'/Users/marti/Desktop/data_analyst_portfolio/python/CMC_API.csv', header='column_names')
    else:
        df.to_csv(r'/Users/marti/Desktop/data_analyst_portfolio/python/CMC_API.csv', mode='a', header=False)


#Importing packages to allow for the time to be displayed for each API pull
import os
from time import time 
from time import sleep

for i in range(333):
    api_runner()
    print('API pull completed')
    sleep(60) #sleep for 1 minute
exit()

#Setting the default format for numbers to float 
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#Using group by on the coin name the better organise the dataframe
df3 = df.groupby('name', sort=False)['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d'].mean()
df3



#Transposing the dataframe in preparation for creating visualisations
df4 = df3.stack()
df4
type(df4)


#Converting the dataframe data type to a dataframe from a series
df5 = df4.to_frame(name='values')
df5


#Changing the index of the dataframe to a standard number format instead of using the 'name' column
index = pd.Index(range(90))
df6 = df5.reset_index()
df6


#Renaming 'level_1' column to percent_change
df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


#Renaming the values in the 'precent_change' column in shorthand for cleaner visualisations
df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d'], ['1h', '24h', '7d','30d'])
df7


#Importing packages for visualisations of the dataframes
import seaborn as sns
import matplotlib.pyplot as plt


#Creating a visualisation showing cryptocurrency performance over the time
sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')
plt.show()


#Querying Bitcoin only from the dataframe
df8 = df[['name', 'quote.USD.price', 'timestamp']]
df8 = df8.query("name == 'Bitcoin'")
df8