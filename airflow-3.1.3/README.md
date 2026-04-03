
# Set up Airflow local instance

<!-- markdownlint-disable MD007-->

<!-- TOC -->

- [Set up Airflow local instance](#set-up-airflow-local-instance)
    - [Set up virtual environment with the correct python version & activate it](#set-up-virtual-environment-with-the-correct-python-version--activate-it)
    - [Fetch docker-compose.yaml from the official docs](#fetch-docker-composeyaml-from-the-official-docs)
        - [Ensure the docker-compose file uses image compatible with your python installation](#ensure-the-docker-compose-file-uses-image-compatible-with-your-python-installation)
            - [Apache Airflow 2.9.3 is compatible with the following Python versions](#apache-airflow-293-is-compatible-with-the-following-python-versions)
    - [Set up the right Airflow user](#set-up-the-right-airflow-user)
    - [Initialize airflow.cfg with default values](#initialize-airflowcfg-with-default-values)
    - [Spin up the local instance](#spin-up-the-local-instance)
        - [gracefully stop the local instance](#gracefully-stop-the-local-instance)
    - [References](#references)

<!-- /TOC -->

## Set up virtual environment with the correct python version & activate it

```bash
# 3.1.3
python3.12 -m venv airflow-3.1.1
source airflow-3.1.1/bin/activate
```

## Fetch `docker-compose.yaml` from the official docs

```bash
# 3.1.3
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.3/docker-compose.yaml'
```

### Ensure the docker-compose file uses image compatible with your python installation

#### Apache Airflow 2.9.3 is compatible with the following Python versions

| Python Version | Status in Airflow 2.9.3 | Notes |
| --- | --- | --- |
| **3.8** | Supported | N/A |
| **3.9** | Supported | N/A |
| **3.10** | Supported | **Recommended** for high stability. |
| **3.11** | Supported | **Recommended** for performance/stability balance. |
| **3.12** | Supported | Requires `pendulum>=3.0.0`. |
| **3.13+** | **Not Supported** | Support for 3.13+ is not available in the 2.9.x series. |

For the official `apache/airflow:2.9.3` Docker image (without a suffix), the default Python version is **Python 3.12**

If you pull the following tags, here is what you get:

| Tag | Resulting Python Version |
| --- | --- |
| `apache/airflow:2.9.3` | **Python 3.12** (Default) |
| `apache/airflow:2.9.3-python3.11` | Python 3.11 |
| `apache/airflow:2.9.3-python3.8` | Python 3.8 |

Recommendation is to change your default `docker-compose` file to use `apache/airflow:2.9.3-python3.11`

```bash
${AIRFLOW_IMAGE_NAME:-apache/airflow:2.9.3-python3.11}
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

- [Airflow 3.1.3](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
