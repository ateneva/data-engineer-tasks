# Data Engineering Solution

<!-- TOC -->

- [Data Engineering Solution](#data-engineering-solution)
    - [Local Setup](#local-setup)
    - [Data Setup](#data-setup)

<!-- /TOC -->

## Local Setup

`docker-compose.yml` creates a local Airflow instance from the official image published on Docker Hub

It is useful to be able to spin up a local instance as a way of DAG testing

To do so, you need to run the snippet below:

```bash
docker compose --file docker-compose.yml up
```

## Data Setup

Assumption is that data is received from another team that going forward will regularly place 2 distinct files in a GCS bucket for us to consume

To faciliate this assumption, the files have been uploaded in `eu-data-challenge/data_engineer` and `eu-data-challenge/usa_median_household_income` respectively using `gcs-upload-object-from-file.py`

Needed GCP resources can be re-created using the setups provided in folder `terraform`
