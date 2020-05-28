# Covid Economic Dashboard
This project was to showcase the volatility in the economy and how Covid-19 has directly affected the economy of Malaysia since the start of the pandemic. Stock prices of public listed companies were tracked during the period of this pandemic in various sectors. It was a simple project to practice my data engineering skills.


## Architecture 
Architecture-Image:
![alt text](https://github.com/dazza10/Covid-Economic-Dashboard/blob/master/Images/AWS%20(2019)%20horizontal%20framework.png)



## Project Installation
1. Install and update all packages as per the requirements.txt in your environment using the [pip ](https://www.startdataengineering.com/ "Pip Installation") command: 

- For example;

- ```pip install pandas== ```

2. Database used for this project was MYSQL database. Therefore all python-sql connectors used were for the MYSQL database. Please amend the codes as per your database used.


3. There is a file named secrets.py in the covid_project folder. Please open the file and fill up the database connection details and save the file. Ensure the secrets.py file is saved in the same folder as all the other working files.

4. Run the file name ddl.py first to create schemas in the MYSQL database.

5. Other _.py_ files can be initiated in any order.



## Roadmap
- Add a Twitter Live Streaming of Data into the Database (Python Twitter Packages)
- Use Airflow to bring all processes together
- Performing sentiment Analysis on the Tweets (Machine Learning)
- Deploying these ML models on the cloud
- Creating a Frontend UI for users to visualize this data (Django, Flask)



