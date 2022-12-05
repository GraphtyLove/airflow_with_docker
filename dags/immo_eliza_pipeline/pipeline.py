from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from uuid import uuid4
import os


default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Data pipeline for immo eliza',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 11, 21),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=1)
}

with DAG('immo-eliza-pipeline', default_args=default_args, schedule_interval="30 * * * *", catchup=False) as dag:

    pipeline_id = str(uuid4())

    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        
        
    task_1 = DockerOperator(
        task_id='scraping',
        image='airflow_scraper:latest',
        container_name='task___scraper',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "AZURE_CONTAINER_NAME": os.getenv("AZURE_CONTAINER_NAME"),
            "CUSTOM_PIPELINE_ID": pipeline_id
        }
        )

    task_2 = DockerOperator(
        task_id='cleaning',
        image='airflow_data_cleaner:latest',
        container_name='task___cleaning',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        
        environment= {
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "AZURE_CONTAINER_NAME": os.getenv("AZURE_CONTAINER_NAME"),
            "CUSTOM_PIPELINE_ID": pipeline_id
        }
        )

    task_3 = BashOperator(
        task_id='print_done',
        bash_command='echo "All done!"'
    )

    start_dag >> task_1 
    
    task_1 >> task_2 >> task_3

    task_3 >> end_dag