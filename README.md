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

## Data Setup

### Assumptions/Givens

Assumption is that data is received from another team that going forward will regularly place 2 distinct files in a GCS bucket for us to consume

To faciliate this assumption, the files have been uploaded in `eu-data-challenge/data_engineer` and `eu-data-challenge/usa_median_household_income` respectively using `gcs-upload-object-from-file.py`
