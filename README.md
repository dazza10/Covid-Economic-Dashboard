# Covid Economic Dashboard

This project was to showcase the volatility in the economy and how Covid-19 has directly affected the economy of Malaysia since the start of the pandemic. Stock prices of public listed companies were tracked during the period of this pandemic in various sectors. It was a simple project to practice my data engineering skills.

## Architecture

Architecture-Image:
![alt text](https://github.com/dazza10/Covid-Economic-Dashboard/blob/master/Images/AWS%20(2019)%20horizontal%20framework.png)

## Project Installation

1. Python version 3.7.5 was used for this project.

2. Install and update all packages as per the requirements.txt in the covid_project folder in your environment using the [pip ](https://www.startdataengineering.com "Pip Installation") command:

   ```pip install -r requirements.txt```

3. Database used for this project was MYSQL database. Therefore all python-sql connectors used were for the MYSQL database. Please amend the codes as per your database used.

4. There is a file named secrets.py in the covid_project folder. Please open the file and fill up the local  database connection details (in my case MYSQL) and save the file. Ensure the secrets.py file is saved in the same folder as all the other working files. (**IMPORTANT**)

5. Open the ddl.py and fill up "psswd" by replacing the _XXX_. (**IMPORTANT**) Run the file name ddl.py first before all the other files to create schemas in the MYSQL database.

6. Other _.py_ files in the covid_project folder can be initiated in any order.

## Usage

1. **ddl.py** - Creates the schemas/tables in MYSQL.

2. **daily_stats.py** - Calls from an API; daily stats of the coronavirus.

3. **news.py** - Calls from an API; the updated news in relation to the pandemic.

4. **stocks.py** - Calls from an API; the daily updated stock prices of public listed companies.

5. **gainer.py** - Scrapes from a website; compiles the companies that increased the most in terms of price from previous working day.

6. **loser.py** - Scrapes from a website; compiles the companies that decreased the most in terms of price from previous working day.

7. **volume.py** - Scrapes from a website; compiles the companies that had the most trading volume from previous working day.

8. **secrets.py** - A file to input your relational database login credentials to connect to your local database.

## Roadmap

My Goals Moving Forward for this Project

- Add a Twitter Live Streaming of Data into the Database (Python Twitter Packages)
- Use Airflow to bring all processes together
- Performing sentiment Analysis on the Tweets (Machine Learning)
- Deploying these ML models on the cloud
- Creating a Frontend UI for users to visualize this data (Django, Flask)
