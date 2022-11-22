#!/bin/bash

# Build Docker images
docker build -f dags/immo_eliza_pipeline/scraper/Dockerfile -t airflow_scraper:latest ./dags/immo_eliza_pipeline/scraper;
docker build -f dags/immo_eliza_pipeline/data_cleaner/Dockerfile -t airflow_data_cleaner:latest ./dags/immo_eliza_pipeline/data_cleaner;

# Run Airflow
docker-compose up -d;