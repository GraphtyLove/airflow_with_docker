# Airflow with Docker

![Airflow](https://airflow.apache.org/images/feature-image.png)


[Apache Airflow](https://airflow.apache.org/) is a pipeline system to manage jobs.
It’s mainly used to create data-pipeline systems.

This is used a lot in the industry because of its ability to structure code execution. You can also find a lot of tools that are based on Airflow, so mastering this tool will help you with others. [Kubeflow](https://www.kubeflow.org/) is a great example of that.


We will use Docker to run Airflow. This is a great way to run Airflow because it will allow you to run it in any environment. You can run it in your local machine, in a server, or even in a cloud provider.

Let's see how we can do that.

## Requirements
- Docker installed and running
- Docker Compose installed


## Usage
Execute the starting script that will:

1. Build the Docker image for each task
2. Start Airflow

```bash
bash ./scripts/start.sh
```


## Resources
- [Article explaining the flow](https://towardsdatascience.com/using-apache-airflow-dockeroperator-with-docker-compose-57d0217c8219)
- [Link github repo with more complex example](https://github.com/fclesio/airflow-docker-operator-with-compose)