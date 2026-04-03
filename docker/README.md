
# Docker

<!-- markdownlint-disable MD007 -->

<!-- TOC -->

- [Docker](#docker)
- [Images](#images)
    - [Pulling image from DockerHub](#pulling-image-from-dockerhub)
    - [Building images](#building-images)
        - [creating image from a container](#creating-image-from-a-container)
    - [Pushing image to DockerHub](#pushing-image-to-dockerhub)
        - [Pushing image to Container Registry GCP](#pushing-image-to-container-registry-gcp)
        - [Pushing image to ECS AWS](#pushing-image-to-ecs-aws)
    - [Removing Tags](#removing-tags)
- [Containers](#containers)
    - [Building Re-creating containers](#building-re-creating-containers)
        - [copy all files from a local folder to existing container](#copy-all-files-from-a-local-folder-to-existing-container)
        - [Execute a command on a running container](#execute-a-command-on-a-running-container)
        - [handy container commands](#handy-container-commands)
- [References](#references)

<!-- /TOC -->

<!-- markdownlint-disable MD025 -->

# Images

```bash
docker image ls -a                         # list all docker images
docker image ls                            # list the images in the local repo
docker image rm <image id>                 # remove a docker image
docker image rm $(docker image ls -a -q)   # remove image on windows
```

## Pulling image from DockerHub

```bash
# latest image
docker pull tenevaa/mysql-dvd-rentals:latest

# earlier image
docker pull apache/airflow:2.9.3-python3.11
```

## Building images

```bash
docker build -t <image name> .            # create the image
```

### [creating image from a container](https://www.dataset.com/blog/create-docker-image/)

```bash
# create an image from a container
docker commit <container name>
docker commit mysql_dvd_rental_1

# check images
docker image ls

# tag the newly-created image
docker tag <image id> <tag name>
docker tag 6857a570e647 mysql-dvd
```

```text
angelina.teneva@Angelinas-MacBook-Pro mysql % docker commit mysql_dvd_rental_1
sha256:6857a570e647eecd7a2c97bd717efbaab2de031a58cb4972586aff1563c5c090
angelina.teneva@Angelinas-MacBook-Pro mysql % docker image ls
REPOSITORY               TAG       IMAGE ID       CREATED          SIZE
<none>                   <none>    6857a570e647   42 seconds ago   546MB
postgres                 latest    0c3f88e824de   7 days ago       357MB
mysql                    latest    262f364f4f01   9 days ago       546MB
adminer                  latest    f0aa9b7b3eec   2 weeks ago      80.8MB
mysql/mysql-server       latest    e588e8734686   2 months ago     471MB
docker/getting-started   latest    157095baba98   6 months ago     27.4MB
angelina.teneva@Angelinas-MacBook-Pro mysql %

angelina.teneva@Angelinas-MacBook-Pro mysql % docker image ls
REPOSITORY               TAG       IMAGE ID       CREATED         SIZE
mysql-dvd                latest    6857a570e647   8 minutes ago   546MB
postgres                 latest    0c3f88e824de   7 days ago      357MB
mysql                    latest    262f364f4f01   9 days ago      546MB
adminer                  latest    f0aa9b7b3eec   2 weeks ago     80.8MB
mysql/mysql-server       latest    e588e8734686   2 months ago    471MB
docker/getting-started   latest    157095baba98   6 months ago    27.4MB
angelina.teneva@Angelinas-MacBook-Pro mysql %
```

```bash
# create an image from a container and tag it
docker commit <container name> <tag name>
docker commit mysql_dvd_rental_1 mysql-dvd-rental
```

```text
angelina.teneva@Angelinas-MacBook-Pro mysql % docker image ls
REPOSITORY               TAG       IMAGE ID       CREATED         SIZE
mysql-dvd-rental         latest    6b04072b74af   3 seconds ago   546MB
mysql-dvd                latest    6857a570e647   9 minutes ago   546MB
postgres                 latest    0c3f88e824de   7 days ago      357MB
mysql                    latest    262f364f4f01   9 days ago      546MB
adminer                  latest    f0aa9b7b3eec   2 weeks ago     80.8MB
mysql/mysql-server       latest    e588e8734686   2 months ago    471MB
docker/getting-started   latest    157095baba98   6 months ago    27.4MB
```

## [Pushing image to DockerHub](https://docs.docker.com/docker-hub/repos/)

```bash
# the image must be tagged as follows
docker build -t <hub-user>/<repo-name>[:<tag>]

docker push <hub-user>/<repo-name>:<tag>
docker push tenevaa/mysql-dvd-rentals:mysql-dvd
```

### [Pushing image to Container Registry (GCP)](<https://cloud.google.com/container-registry/docs/pushing-and-pulling>)

```bash
docker pull busybox
docker tag busybox gcr.io/my-project/busybox
docker push gcr.io/my-project/busybox
```

### Pushing image to ECS (AWS)

```bash
```

## [Removing Tags](https://docs.docker.com/engine/reference/commandline/rmi/)

```text
angelina.teneva@Angelinas-MacBook-Pro mysql % docker image ls
REPOSITORY                  TAG       IMAGE ID       CREATED        SIZE
mysql-dvd-rentals           latest    6b04072b74af   8 days ago     546MB
tenevaa/mysq-dvd-rentals    latest    6b04072b74af   8 days ago     546MB
tenevaa/mysql-dvd-rentals   latest    6b04072b74af   8 days ago     546MB
mysql-dvd-rental            latest    6b04072b74af   8 days ago     546MB
mysql-dvd                   latest    6857a570e647   8 days ago     546MB
postgres                    latest    0c3f88e824de   2 weeks ago    357MB
mysql                       latest    262f364f4f01   2 weeks ago    546MB
adminer                     latest    f0aa9b7b3eec   3 weeks ago    80.8MB
mysql/mysql-server          latest    e588e8734686   3 months ago   471MB
docker/getting-started      latest    157095baba98   6 months ago   27.4MB
```

```bash
docker rmi <tag>

docker rmi tenevaa/mysq-dvd-rentals
docker rmi mysql-dvd-rentals
docker rmi
docker rmi mysql-dvd-rental
```

```text
angelina.teneva@Angelinas-MacBook-Pro mysql % docker image ls
REPOSITORY                  TAG       IMAGE ID       CREATED        SIZE
tenevaa/mysql-dvd-rentals   latest    6b04072b74af   8 days ago     546MB
mysql-dvd                   latest    6857a570e647   8 days ago     546MB
postgres                    latest    0c3f88e824de   2 weeks ago    357MB
mysql                       latest    262f364f4f01   2 weeks ago    546MB
adminer                     latest    f0aa9b7b3eec   3 weeks ago    80.8MB
mysql/mysql-server          latest    e588e8734686   3 months ago   471MB
docker/getting-started      latest    157095baba98   6 months ago   27.4MB
angelina.teneva@Angelinas-MacBook-Pro mysql %
```

<!-- markdownlint-disable MD025 -->

# Containers

```bash
docker container ls                       # list all running containers
docker container ls -a                    # list all containers
docker container stop <container id>      # gracefuly stop containers
docker container kill <container id>      # force quit containers
docker container rm <container id>        # delete containers
docker container run <image name>         # run the image
docker container run -it <image name>     # run the image and interact with it

# run an image called olympics
docker container run olympics

# run the olympics image on a a specific port
docker container run -p 8888:8888 olympics

# run the image called `bash` by using
docker container run -it -v "%cd%": /data dev-env bash
```

- <https://docs.docker.com/engine/reference/commandline/container_rm/>

- <https://docs.docker.com/engine/reference/commandline/container_run/>

## Building (Re-creating) containers

```bash
docker-compose -f docker-compose.yml up
docker-compose -f docker-compose.yml up --force-recreate
```

- <https://docs.docker.com/compose/reference/up/>

- <https://stackoverflow.com/questions/52106464/what-is-the-difference-between-the-build-and-force-recreate-flags-to-do>

- <https://stackoverflow.com/questions/47081505/docker-compose-force-recreate-specific-service>

### copy all files from a local folder to existing container

```bash
# copy a single file from a local folder to a folder inside existing container
docker cp ./src/build/index.html <container name>:/app/

# copy all files from a local folder to a folder inside existing container
docker cp <local path>. <container name>:/<folder on container>/
docker cp /Users/angelina.teneva/Documents/postgres/sample_db/. postgres_dvd_rental_1/:/home/
```

- <https://stackoverflow.com/questions/32566624/docker-cp-all-files-from-a-folder-to-existing-container-folder>

### Execute a command on a running container

```bash
#start the container
docker run --name ubuntu_bash --rm -i -t ubuntu bash

# make files from host machine available on container
docker run -v /host_dir:/container_dir ...

### execute a command on a running container
docker exec -d ubuntu_bash touch /tmp/execWorks

### execute an interactive command
docker exec -it ubuntu_bash bash
```

[**Note:**](https://stackoverflow.com/questions/27673563/how-to-get-into-psql-of-a-running-postgres-container)

- `docker exec` runs the command on a running container
- `docker run` will start a new container.

- <https://docs.docker.com/engine/reference/commandline/exec/>

### handy container commands

```bash
# run psql inside a postgresql container
docker exec -ti <container id> psql -U user database
docker exec -ti <container name> psql -U user database
docker exec -ti postgres_dvd_rental_1 psql -U ateneva dvd
```

# References
