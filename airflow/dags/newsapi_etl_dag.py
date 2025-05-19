# airflow/dags/news_etl_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import requests
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Set default arguments
default_args = {
    'owner': 'sohail',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

load_dotenv()

# Read API key from environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Define your ETL functions
def extract_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    
    # Save as a temporary CSV for downstream tasks
    df = pd.json_normalize(articles)
    df.to_csv("/opt/airflow/tmp/news_data.csv", index=False)

def transform_news():
    df = pd.read_csv("/opt/airflow/tmp/news_data.csv")
    # Simple transformation (e.g., select columns)
    df = df[['title', 'description', 'publishedAt', 'url']]
    df.dropna(inplace=True)
    df.to_csv("/opt/airflow/tmp/news_data_clean.csv", index=False)

def load_news():
    df = pd.read_csv("/opt/airflow/tmp/news_data_clean.csv")

#     conn = psycopg2.connect(
#     user="postgres",
#     password="Sohail123",
#     host="host.docker.internal",  # NOT localhost from inside Docker
#     database="newsdb",
#     port=5432
# )

    conn = psycopg2.connect(
        host='postgres',
        dbname='airflow',
        user='airflow',
        password='airflow',
        port=5432
    )

    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            published_at TIMESTAMP,
            url TEXT
        )
    """)
    
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO news (title, description, published_at, url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (row['title'], row['description'], row['publishedAt'], row['url']))

    conn.commit()
    cur.close()
    conn.close()

# Define the DAG
with DAG(
    dag_id='news_etl_dag',
    default_args=default_args,
    description='ETL pipeline for NewsAPI with Airflow',
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id='extract_news',
        python_callable=extract_news
    )

    task_transform = PythonOperator(
        task_id='transform_news',
        python_callable=transform_news
    )

    task_load = PythonOperator(
        task_id='load_news',
        python_callable=load_news
    )

    task_extract >> task_transform >> task_load
