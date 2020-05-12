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
news_updated = (response.json())
news = json_normalize(news_updated['items'])
news.drop(columns=['language','countryCode','status'],inplace=True)

symbol=['AMZN','MSFT','FB','GOOGL','BABA']

full = []
def stock_response(base_url):
    for sym in symbol:
        parameter={'function':'TIME_SERIES_INTRADAY','symbol':sym,'interval':'60min','outputsize':'compact','datatype':'csv',
          'apikey':'E9W1BV42Y27SB9E9'}
        r = requests.get(base_url,params=parameter)
        dataFrame = pd.read_csv(StringIO(r.text),sep=",")
        dataFrame = dataFrame.rename(columns={'timestamp':'DateTime','open':'Open($)','high':'High($)','low':'Low($)',
                                              'close':'Close($)','volume':'Volume'})
        dataFrame['Company']=sym
        full.append(dataFrame)
        print(full)
    final = pd.concat(full,ignore_index=True)
    return final
    
df = (stock_response('https://www.alphavantage.co/query'))

df['DateTime']=pd.to_datetime(df['DateTime'])
price_date = df['DateTime']
price_close = df['Close($)']

grid = sns.FacetGrid(df, 'Company' , height=5 , aspect = 3 ,sharey=False)
grid.map(sns.lineplot, 'DateTime','Close($)', palette = 'deep'  )
plt.gcf().autofmt_xdate()
axes=grid.axes
axes[0,0].set(ylim=(2200,None))
axes[1,0].set(ylim=(150,None))
axes[2,0].set(ylim=(150,None))
axes[3,0].set(ylim=(1000,None))
axes[4,0].set(ylim=(150,None))
plt.xlabel('Date')
plt.tight_layout()


#Writing code to database
