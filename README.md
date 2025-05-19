# 📰 NewsAPI ETL Pipeline with Apache Airflow, Docker & PostgreSQL

This project demonstrates a full **ETL (Extract, Transform, Load)** pipeline using **Apache Airflow**, **Docker**, and **PostgreSQL**. It fetches top US headlines from the NewsAPI, transforms and cleans the data using Pandas, and loads it into a PostgreSQL database.

---

## 📌 Features

- ⛏️ **Extract**: Fetches real-time headlines from [NewsAPI.org](https://newsapi.org/)
- 🔄 **Transform**: Cleans and selects relevant fields using Pandas
- 📥 **Load**: Inserts the data into a PostgreSQL table
- ⚙️ **Scheduled & Automated**: Runs hourly via Apache Airflow DAG
- 🐳 **Dockerized**: Completely containerized setup with Docker & Docker Compose

---

## 🛠️ Tech Stack

| Tool                                               | Usage                                |
| -------------------------------------------------- | ------------------------------------ |
| [Apache Airflow](https://airflow.apache.org/)      | Orchestrates ETL tasks as DAGs       |
| [Docker](https://www.docker.com/) + Docker Compose | Containerizes Airflow and PostgreSQL |
| [NewsAPI](https://newsapi.org/)                    | Source of news articles              |
| [PostgreSQL](https://www.postgresql.org/)          | Target database                      |
| [Pandas](https://pandas.pydata.org/)               | Data transformation                  |

---

## 📁 Project Structure

airflow_docker_etl_project/
├── airflow/
│ ├── dags/
│ │ └── news_etl_dag.py
│ ├── plugins/
│ ├── tmp/
├── .env # Contains NEWS_API_KEY
├── docker-compose.yml
├── README.md

🖼️ Screenshot
- View the Screenshot.png for working Airflow DAG.

🗃️ Sample Table Schema

CREATE TABLE IF NOT EXISTS news (
id SERIAL PRIMARY KEY,
title TEXT,
description TEXT,
published_at TIMESTAMP,
url TEXT
);

🤝 Credits

NewsAPI : https://newsapi.org/
Apache Airflow Docs : https://airflow.apache.org/docs/
Docker : https://www.docker.com/
