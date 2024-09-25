# Data Engineering Solution

## Setup for local testing

### create virtual environment

```bash
python3 -m venv apache_airflow
source apache_airflow/bin/activate
```

### spin up local airflow instance

`docker-compose.yml` creates a local Airflow instance from the official image published on Docker Hub

It is useful to be able to spin up a local instance as a way of DAG testing

To do so, you need to run the snippet below:

```bash
docker compose --file docker-compose.yml up
```
