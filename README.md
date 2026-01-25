
# Set up Airflow local instance

<!-- markdownlint-disable MD007-->

<!-- TOC -->

- [Set up Airflow local instance](#set-up-airflow-local-instance)
    - [Fetch docker-compose.yaml from the official docs](#fetch-docker-composeyaml-from-the-official-docs)
    - [Set up the right Airflow user](#set-up-the-right-airflow-user)
    - [Initialize airflow.cfg with default values](#initialize-airflowcfg-with-default-values)
    - [Spin up the local instance](#spin-up-the-local-instance)
        - [gracefully stop the local instance](#gracefully-stop-the-local-instance)
    - [References](#references)

<!-- /TOC -->

## Fetch `docker-compose.yaml` from the official docs

```bash
# 2.9.3
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.3/docker-compose.yaml'

# 3.1.3
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.3/docker-compose.yaml'
```

## Set up the right Airflow user

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## Initialize `airflow.cfg` with default values

- uncomment `AIRFLOW_CONFIG` from `docker-compose` file and run

```bash
docker compose --file docker-compose.yml run airflow-cli airflow config list
```

## Spin up the local instance

You can test a DAG locally by spinning up a local airflow instance using `docker compose`

```bash
docker compose --file docker-compose.yml up
```

You should be able to access Airflow UI on <http://localhost:8080>

### gracefully stop the local instance

Once finished testing, you can bring down your airflow instance by running

```bash
docker compose --file docker-compose.yml down
```

---

## References

- [Airflow 2.9.3](https://airflow.apache.org/docs/apache-airflow/2.9.3/howto/docker-compose/index.html)

- [Airflow 3.1.3](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
