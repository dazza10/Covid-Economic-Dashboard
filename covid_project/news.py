"""
Airflow DAGS

"""
import pandas as pd
from datetime import datetime
from pandas.io.json import json_normalize
import requests
from google.cloud import storage
import os

from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from google.cloud import bigquery


def news_func():

    # Pulling some news from news api from the same website
    response = requests.get(
        "http://api.coronatracker.com/news/trending", params={"country": "Malaysia"}
    )
    news_updated = response.json()
    news = json_normalize(news_updated["items"])
    news.drop(columns=["language", "countryCode", "status", "author"], inplace=True)
    news["publishedAt"] = pd.to_datetime(news["publishedAt"])
    news["addedOn"] = pd.to_datetime(news["addedOn"])
    news.drop_duplicates(subset="nid", keep="first", inplace=True)
    news.to_csv(r"/home/dharrankandaiah/tmp/news.csv", index=False)


def delete_tmp_file():
    myfile = "/home/dharrankandaiah/tmp/news.csv"

    try:
        os.remove(myfile)
    except OSError as e:
        print("Error : %s - %s." % (e.filename, e.strerror))


def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client.from_service_account_json(
        "/home/dharrankandaiah/key.json"
    )
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


def upload_to_bq():
    client = bigquery.Client.from_service_account_json("/home/dharrankandaiah/key.json")
    dataset_ref = client.dataset("covid_19")
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://bucket_covid/news.csv"
    load_job = client.load_table_from_uri(
        uri, dataset_ref.table("news"), job_config=job_config
    )
    load_job.result()
    destination_table = client.get_table(dataset_ref.table("news"))
    print("loaded {} row.".format(destination_table.num_rows))


default_args = {
    "start_date": datetime(2020, 6, 15),
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="news_call",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    t1 = DummyOperator(task_id="dummy_task", retries=3)

    t2 = PythonOperator(task_id="news_task", python_callable=news_func, retries=2)

    t3 = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_bucket,
        op_kwargs={
            "bucket_name": "bucket_covid",
            "source_file_name": "/home/dharrankandaiah/tmp/news.csv",
            "destination_blob_name": "news.csv",
        },
        retries=2,
    )

    t4 = PythonOperator(
        task_id="delete_tmp_file", python_callable=delete_tmp_file, retries=2
    )

    t5 = PythonOperator(task_id="upload_to_bq", python_callable=upload_to_bq, retries=2)

    # t5 = GoogleCloudStorageToBigQueryOperator(
    #     task_id="staging_covid",
    #     bucket="bucket_covid",
    #     source_objects=["news.csv"],
    #     destination_project_dataset_table="covid-19-dashboard-1010:covid_19.news",
    #     write_disposition="WRITE_TRUNCATE",
    #     skip_leading_row=1,
    #     bigquery_conn_id="bigquery_covid",
    #     google_cloud_storage_conn_id="google_cloud_covid",
    # )

    t1 >> t2 >> t3 >> t4 >> t5

