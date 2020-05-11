#importing all packages
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from matplotlib import dates as mpl_dates

#defining the function to pull api from website
def response(base_url):
    paramater= {'startDate':'2020-05-06','endDate':'2020-05-11','countryCode':'MY'}
    r = requests.get(base_url, params=paramater)
    dataframe = pd.DataFrame(r.json())
    return dataframe
 
#getting live data & new cases and merging them into single dataFrame
live = response('http://api.coronatracker.com/v3/analytics/trend/country')
new_case = response('http://api.coronatracker.com/v3/analytics/newcases/country')
merged = pd.concat([live,new_case],axis=1)

#pulling some news from news api from the same website
response = requests.get('http://api.coronatracker.com/news/trending', params={'country':'Malaysia'})
news_updated = response.json()
news = pd.DataFrame(json_normalize(news_updated))
