import pandas as pd
import requests
from bs4 import BeautifulSoup


url = "https://www.klsescreener.com/v2/markets"
page = requests.get(url)
html= page.content
soup = BeautifulSoup(html,'html.parser')


active = soup.find_all(class_="row equal")
company_vol=[]
num_vol=[]

for name in active[1].find_all(class_="col-md-4"):
    company = name.find("a").get_text()
    company_vol.append(company)

for vol in active[1].find_all(class_="col-sm-5 text-right"):
    volume = vol.get_text()
    num_vol.append(volume)

df = pd.DataFrame({
    'Stock':company_vol,
    'Volume':num_vol
})

df["Volume"] = df['Volume'].apply(lambda x:x.split('\n')[1]) 


