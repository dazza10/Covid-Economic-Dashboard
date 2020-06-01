'''
First code is to define a general function used to pull different data from the same website.
Second code is to pull the data of corona cases on a daily basis

'''
import pandas as pd
import datetime
import requests
import secrets
import sqlalchemy

#Defining the function to pull api from website
def response(base_url):
    paramater= {'startDate':(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),
                'endDate':(datetime.datetime.now().strftime('%Y-%m-%d')),'countryCode':'MY'}
    r = requests.get(base_url, params=paramater)
    print(r)
    dataframe = pd.DataFrame(r.json())
    return dataframe
 
#Getting data of existing cases.
live = response('http://api.coronatracker.com/v3/analytics/trend/country')

#Getting new cases occuring on a daily.
new_case = response('http://api.coronatracker.com/v3/analytics/newcases/country')

#Data cleansing to combine both the data and drop some columns.
new_case.drop(columns='last_updated',inplace=True)
daily_stats = pd.concat([live,new_case],axis=1)
daily_stats.drop(columns=['country_code','country'],inplace=True)
daily_stats[['Date','Time']] = daily_stats['last_updated'].str.split('T',expand=True)
daily_stats.drop(columns=['last_updated','Time'],inplace=True)
daily_stats.rename(columns={'total_confirmed':'Total_Confirmed','total_deaths':'Total_Deaths',
                           'total_recovered':'Total_Recovered','new_infections':'New_Infections',
                           'new_deaths':'New_Deaths','new_recovered':'New_Recovered'},inplace=True)
daily_stats['Date']=pd.to_datetime(daily_stats['Date'])


#Ceating a connection between SQL Database and python using SQL Alchemy

conn= "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)
engine = sqlalchemy.create_engine(conn)

# Pushing Data to MySQL
daily_stats.to_sql(name='daily_stats',con=engine, index=False,if_exists='append')
