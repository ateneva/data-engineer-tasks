# Spinning up Airflow Astronomer

<!-- markdownlint-disable MD007-->

<!-- TOC -->

- [Spinning up Airflow Astronomer](#spinning-up-airflow-astronomer)
    - [Pre-requisites](#pre-requisites)
        - [setup virual environment & activate it](#setup-virual-environment--activate-it)
        - [install astro cli](#install-astro-cli)
    - [Starting your local instance](#starting-your-local-instance)

<!-- /TOC -->

## Pre-requisites

### setup virual environment & activate it

```bash
python3.10 -m venv astro-2.10.2
source astro-2.10.2/bin/activate
```

### install astro cli

```bash
brew install astro

# install specific version
brew install astro@1.29.0

# check which version is isntalled
astro version

# upgrade astro
brew upgrade astro
```

Your Astro project contains the following files and folders:

- `dags`: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
  - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).

- `Dockerfile`: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.

- `include`: This folder contains any additional files that you want to include as part of your project. It is empty by default.

- `packages.txt`: Install OS-level packages needed for your project by adding them to this file. It is empty by default.

- `requirements.txt`: Install Python packages needed for your project by adding them to this file. It is empty by default.

- `plugins`: Add custom or community plugins for your project to this file. It is empty by default.

- `airflow_settings.yaml`: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

## Starting your local instance

1. Start Airflow on your local machine by running `astro dev start`.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

Running `astro dev start` will start your project with the Airflow Webserver exposed at port `8080` (<http://localhost:8080/>) and Postgres exposed at port `5432` (localhost:5432/postgres)

```bash
# initialize project
astro dev init

# start an instance
astro dev start

# restart an instance
astro dev restart

# stop an instance
astro dev stop
```
