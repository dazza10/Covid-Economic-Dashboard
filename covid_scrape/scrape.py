import requests
from bs4 import BeautifulSoup
import pandas as pd

#def Connecturl():
url = "https://www.klsescreener.com/v2/markets"
page = requests.get(url)
html= page.content
soup = BeautifulSoup(html,'html.parser')


#with open("allPrice.html", "w") as myfile:
    #myfile.write(soup.prettify())

active = soup.find_all(class_="row equal")
company_vol=[]
num_vol=[]

for name in active[1].find_all(class_="col-md-4"):
    company = name.find("a").get_text()
    company_vol.append(company)

for vol in active[1].find_all(class_="col-sm-5 text-right"):
    volume = vol.get_text()
    num_vol.append(volume)

df = pd.DataFrame(list(zip(company_vol,num_vol)))
print(df)