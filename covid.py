#importing all packages
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from matplotlib import dates as mpl_dates
import datetime
import sqlalchemy
import secrets


#defining the function to pull api from website
def response(base_url):
    paramater= {'startDate':(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),
                'endDate':(datetime.datetime.now().strftime('%Y-%m-%d')),'countryCode':'MY'}
    r = requests.get(base_url, params=paramater)
    print(r)
    dataframe = pd.DataFrame(r.json())
    return dataframe
 
#getting live data & new cases and merging them into single dataFrame
live = response('http://api.coronatracker.com/v3/analytics/trend/country')
new_case = response('http://api.coronatracker.com/v3/analytics/newcases/country')
new_case.drop(columns='last_updated',inplace=True)
daily_stats = pd.concat([live,new_case],axis=1)
daily_stats.drop(columns=['country_code','country'],inplace=True)
daily_stats[['Date','Time']] = daily_stats['last_updated'].str.split('T',expand=True)
daily_stats.drop(columns=['last_updated','Time'],inplace=True)
daily_stats.rename(columns={'total_confirmed':'Total_Confirmed','total_deaths':'Total_Deaths',
                           'total_recovered':'Total_Recovered','new_infections':'New_Infections',
                           'new_deaths':'New_Deaths','new_recovered':'New_Recovered'},inplace=True)
daily_stats['Date']=pd.to_datetime(daily_stats['Date'])

#pulling some news from news api from the same website
response = requests.get('http://api.coronatracker.com/news/trending', params={'country':'Malaysia'})
news_updated = (response.json())
news = pd.json_normalize(news_updated['items'])
news.drop(columns=['language','countryCode','status'],inplace=True)
news['publishedAt']=pd.to_datetime(news['publishedAt'])
news['addedOn']=pd.to_datetime(news['addedOn'])
news.drop_duplicates(subset='nid',keep='first',inplace=True)

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
    
stocks = (stock_response('https://www.alphavantage.co/query'))
stocks[['Date','Time']]=stocks['DateTime'].str.split(" ",n=1,expand=True)
stocks=stocks[['DateTime','Date','Time','Open($)','High($)','Low($)','Close($)','Volume','Company']]
stocks=stocks.loc[stocks['Date']==(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')]
stocks['DateTime']=pd.to_datetime(stocks['DateTime'])
stocks['Date']=pd.to_datetime(stocks['Date'])
stocks['Time'] = stocks['Time'].apply(lambda x: datetime.datetime.strptime(x,"%H:%M:%S").time())


grid = sns.FacetGrid(stocks, 'Company' , height=5 , aspect = 3 ,sharey=False)
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


#Ceating a connection between SQL Database and python using SQL Alchemy

conn= "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)
engine = sqlalchemy.create_engine(conn)

# Pushing Data to MySQL
daily_stats.to_sql(name='daily_stats',con=engine, index=False,if_exists='append')
news.to_sql(name='news',con=engine, index=False,if_exists='append')
stocks.to_sql(name='stocks',con=engine, index=False,if_exists='append')

