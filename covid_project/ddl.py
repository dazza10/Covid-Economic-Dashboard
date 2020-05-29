import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    passwd= 'XXX'
    )

mycursor = mydb.cursor()
DB_NAME = 'covid'

def create_database(mycursor):
    try:
        mycursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database : {} ".format(err))
        exit(1)

try:
    mycursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(mycursor)
        print("Database {} created succesfully.".format(DB_NAME))
        mydb.database = DB_NAME
    else:
        print(err)
        exit(1)


sql = '''

CREATE TABLE IF NOT EXISTS daily_stats(
Total_Confirmed INT NOT NULL,
Total_Deaths INT NOT NULL,
Total_Recovered INT NOT NULL,
`new_Infections` INT,
`New_Deaths` INT,
`New_Recovered` INT,
`Date` DATE UNIQUE
);

CREATE TABLE IF NOT EXISTS news(
nid INT NOT NULL UNIQUE PRIMARY KEY,
title VARCHAR(250),
`description` VARCHAR(2000),
content LONGTEXT,
author VARCHAR(250),
url VARCHAR(250),
urlToImage LONGTEXT,
publishedAt DATETIME,
addedon DATETIME,
siteName VARCHAR(250)
);

CREATE TABLE IF NOT EXISTS stocks(
`DateTime` DATETIME,
`Date` DATE,
`Time` TIME,
`Open($)` FLOAT,
`High($)` FLOAT,
`Low($)` FLOAT,
`Close($)` FLOAT,
Volume FLOAT,
Company VARCHAR (50)
);
'''

try:
    mycursor.execute(sql)
except mysql.connector.Error as err:
    print (err.msg)
else:
    print("OK")

mycursor.close()