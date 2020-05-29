import pandas as pd
import requests
from bs4 import BeautifulSoup
import secrets
import sqlalchemy
import datetime


url = "https://www.klsescreener.com/v2/markets"
page = requests.get(url)
html= page.content
soup = BeautifulSoup(html,'html.parser')


active = soup.find_all(class_="row equal")
company_price=[]
num_price=[]

for name in active[5].find_all(class_="col-md-4"):
    company = name.find("a").get_text()
    company_price.append(company)

for pri in active[5].find_all(class_="col-sm-4 text-right"):
    price = pri.get_text()
    num_price.append(price)

df = pd.DataFrame({
    'Stock':company_price,
    'Price':num_price
})

df["Last"] = df['Price'].apply(lambda x:x.split('\n')[1]) 
df["Change"] = df['Price'].apply(lambda x:x.split('\n')[2].split(" ")[0])
df["% Change"] = df['Price'].apply(lambda x:x.split('\n')[2].split(" ")[1])
df.drop(columns=["Price"],inplace =True)
df['Date']=datetime.datetime.now().date().strftime('%d-%m-%Y')

#Creating a connection betwenn python an MYSQL Database
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)
engine = sqlalchemy.create_engine(conn)

# Moving the the Data Base
df.to_sql(name="top_losers",con=engine,index=False,if_exists='append')
