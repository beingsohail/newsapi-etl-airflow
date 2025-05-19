
import requests
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
URL = 'https://newsapi.org/v2/top-headlines'
PARAMS = {
    'country': 'us',
    'apiKey': API_KEY
}



def extract_data():
    try:
        response = requests.get(url=URL, params=PARAMS)
        all_articles = response.json()["articles"]
        df = pd.DataFrame(all_articles)
    except Exception as e:
        print(e)
    
    return df
    

def transform_data():
    df = extract_data()
    df["source_id"] = df["source"].apply(lambda x: x["id"] if isinstance(x, dict) and "id" in x else None)
    df["source_name"] = df["source"].apply(lambda x: x["name"] if isinstance(x, dict) and "name" in x else None)

    cleaned_df = df[["source_id", "source_name", "author", "title", "description", "url", "publishedAt"]]
    cleaned_df["publishedAt"] = pd.to_datetime(cleaned_df["publishedAt"])

    cleaned_df = cleaned_df .dropna(subset=["title", "url"])
    cleaned_df = cleaned_df.drop_duplicates(subset=["url"])

    return cleaned_df


def load_data():
    conn = psycopg2.connect(
        user = "postgres",
        password = "Sohail123",
        host = "localhost",
        database = "newsdb",
    )
    cursor = conn.cursor()

    cleaned_df = transform_data()
    
    for index, row in cleaned_df.iterrows():
        cursor.execute("""
            INSERT INTO news_articles (source_id, source_name, author, title, description, url, publishedAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['source_id'],
        row['source_name'],
        row['author'],
        row['title'],
        row['description'],
        row['url'],
        row['publishedAt']
    ))
        
    conn.commit()
    cursor.close()
    conn.close()
    print("Data Inserted.")


load_data()