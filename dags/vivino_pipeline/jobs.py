from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator


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
    
    # Sanatize the run_id as by default, it contains characters like ":" or "/"
    # Which couldn't be used for docker volume names
    run_id_sanatized = "{{run_id}}".replace(":", "").replace("/", "").replace(".", "")
    # Create a shared volume that can be used by all the tasks
    SHARED_DOCKER_VOLUME = "/tmp/{{run_id}}:/tmp/shared_datadata"    

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
        volumes=[SHARED_DOCKER_VOLUME]
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
        volumes=[SHARED_DOCKER_VOLUME]
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
	    volumes=[SHARED_DOCKER_VOLUME]
    )


    # ----- Pipeline order definition -----
    start_dag >> extract_task >> transform_task >> load_task >> end_dag
