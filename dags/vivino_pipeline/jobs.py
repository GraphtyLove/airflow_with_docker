from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from dotenv import load_dotenv

load_dotenv(".env")


default_args = {
    'owner'                 : 'Becode_Coaches',
    'description'           : 'ETL pipeline for Vivino',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 6, 13),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('vivino-etl-pipeline', default_args=default_args, schedule_interval="30 * * * *", catchup=False) as dag:
    
    start_dag = DummyOperator(task_id='start_dag')
    end_dag = DummyOperator(task_id='end_dag')        
        
    extract_task = DockerOperator(
        task_id='vivino_extract',
        image='vivino_extract:latest',
        container_name='task___extract',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
	    environement={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER")
	    }
    )

    transform_task = DockerOperator(
        task_id='vivino_transorm',
        image='vivino_transform:latest',
        container_name='task___transform',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
	    environement={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER")
	    }
    )
    
    load_task = DockerOperator(
        task_id='vivino_transorm',
        image='vivino_load:latest',
        container_name='task___load',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
	    environement={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER")
	    }
    )

    # Pipeline order
    start_dag >> extract_task >> transform_task >> load_task >> end_dag
