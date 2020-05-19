'''
The code pull news from the same api and do some cleaning and pushing it to mysql database.

'''
import pandas as pd
import datetime
import requests


#Pulling some news from news api from the same website
response = requests.get('http://api.coronatracker.com/news/trending', params={'country':'Malaysia'})
news_updated = (response.json())
news = pd.json_normalize(news_updated['items'])
news.drop(columns=['language','countryCode','status'],inplace=True)
news['publishedAt']=pd.to_datetime(news['publishedAt'])
news['addedOn']=pd.to_datetime(news['addedOn'])
news.drop_duplicates(subset='nid',keep='first',inplace=True)

#Ceating a connection between SQL Database and python using SQL Alchemy

conn= "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)
engine = sqlalchemy.create_engine(conn)

# Pushing Data to MySQL
news.to_sql(name='news',con=engine, index=False,if_exists='append')

