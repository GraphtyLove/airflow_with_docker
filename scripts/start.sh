#!/bin/bash

# Build Docker images
docker build -f dags/immo_eliza_pipeline/scraper/Dockerfile -t airflow_scraper:latest ./dags/immo_eliza_pipeline;
docker build -f dags/immo_eliza_pipeline/data_cleaner/Dockerfile -t airflow_data_cleaner:latest ./dags/immo_eliza_pipeline;

# Init Airflow (Only first time to install everything)
docker compose up airflow-init;

# Run Airflow
docker-compose --env-file .env up -d;