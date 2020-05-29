'''
The code pulls daily stock prices and do some cleaning and pushing it to mysql database.

'''
import pandas as pd
import datetime
import requests
import string
from io import StringIO
import secrets
import sqlalchemy

# Pulling daily prices from these 5 stocks using an api
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
    final = pd.concat(full,ignore_index=True)
    return final
    
stocks = (stock_response('https://www.alphavantage.co/query'))
# Splitting the datetime columns into date and time columns
stocks['Date']=stocks['DateTime'].apply(lambda x: x.split(" ")[0])
stocks['Time']=stocks['DateTime'].apply(lambda x: x.split(" ")[1])
stocks=stocks[['DateTime','Date','Time','Open($)','High($)','Low($)','Close($)','Volume','Company']]
print (stocks)


# Filtering the data to only provide yesterday's prices
stocks=stocks.loc[stocks['Date']==(datetime.datetime.now()+datetime.timedelta(-1)).strftime("%Y-%m-%d")]

# Transforming to datetime
stocks['DateTime']=pd.to_datetime(stocks['DateTime'])
stocks['Date']=pd.to_datetime(stocks['Date'])
# Transforming to time
stocks['Time'] = stocks['Time'].apply(lambda x: datetime.datetime.strptime(x,"%H:%M:%S").time())


#Ceating a connection between SQL Database and python using SQL Alchemy

conn= "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)
engine = sqlalchemy.create_engine(conn)

# Pushing Data to MySQL
stocks.to_sql(name='stocks',con=engine, index=False,if_exists='append')
