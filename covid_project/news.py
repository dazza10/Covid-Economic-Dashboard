"""
Airflow code to read code from airflow and 

"""
import pandas as pd
from datetime import datetime
from pandas.io import json_normalize
import requests
from google.cloud import storage
import os

from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG


def news_func():

    # Pulling some news from news api from the same website
    response = requests.get(
        "http://api.coronatracker.com/news/trending", params={"country": "Malaysia"}
    )
    news_updated = response.json()
    news = json_normalize(news_updated["items"])
    news.drop(columns=["language", "countryCode", "status"], inplace=True)
    news["publishedAt"] = pd.to_datetime(news["publishedAt"])
    news["addedOn"] = pd.to_datetime(news["addedOn"])
    news.drop_duplicates(subset="nid", keep="first", inplace=True)
    news.to_pdf(r'home/dharrankandaiah/tmp/news.csv')

def delete_tmp_file():
    myfile = "/home/dharrankandaiah/tmp/news.csv"

    try:
        os.remove(myfile)
    except OSError as e:
        print ("Error : %s - %s." % (e.filename,e.strerror))

def upload_to_bucket(bucket_name,source_file_name,destination_blob_name):
    storage_client = storage.Client.from_service_account_json('/home/dharrankandaiah/key.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


default_args = {start_date: datetime(2020, 6, 15), owner: "airflow", retries: "1",catchup : False}

with DAG(
    dag_id="news_call", schedule_interval="@daily", default_args=default_args
) as dag:

    news_task = PythonOperator(task_id="news_task", python_callable=news_func)

    delete_task = PythonOperator(task_id='delete_task',python_callable=delete_tmp_file)

    upload_task = PythonOperator(task_id='upload_task',python_callable=upload_to_bucket,
        op_kwargs='bucket_name':'bucket_covid','source_file_name':'/home/dharrankandaiah/tmp/news/csv',
        'destination_blob_name':'news_csv')

    dummy_task = DummyOperator(task_id="dummy_task", retries=3)

    dummy_task >> news_task >> upload_task >> delete_task
