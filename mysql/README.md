
# Setting up MySQL DB

<!-- markdownlint-disable MD007 -->

<!-- TOC -->

- [Setting up MySQL DB](#setting-up-mysql-db)
    - [with mysql](#with-mysql)
    - [create a custom docker image](#create-a-custom-docker-image)
    - [Loading sample mysql databases](#loading-sample-mysql-databases)
        - [dvd_rental](#dvd_rental)
        - [sakila](#sakila)
        - [employees](#employees)
        - [world_x](#world_x)
    - [References](#references)

<!-- /TOC -->

## with `mysql`

- `python3` [is installed](<https://github.com/ateneva/data-engineer-in-training#install-different-python-versions>)

- `pip` [is installed](<https://github.com/ateneva/data-engineer-in-training#use-brew-to-install-pip-and-virtualenv>)

- [virtual env is in place](<https://github.com/ateneva/how-to-snippets#create-virtual-environment-with-a-particular-python-version>)

- `mysql` [CLI is installed](<https://github.com/ateneva/data-engineer-in-training#install-mysql>)

## create a custom `docker` image

- pull latest official docker image

```bash
docker pull mysql
```

- verify the image exists on your machine

```bash
docker image ls -a
```

- prepare a `yml` file

```yml
version: '3.1'

services:
  dvd_rental:
    image: mysql
    restart: always
    command: --default-authentication-plugin=mysql_native_password
    ports: 
      - "3306:3306"
    hostname: '%'
    environment:
      MYSQL_ROOT_PASSWORD: rentals
      MYSQL_USER: ateneva
      MYSQL_PASSWORD: ateneva_rentals
      MYSQL_DATABASE: dvd
      DATA: /var/lib/mysql
    volumes: 
      - /var/lib/mysql
```

- deploy and start the container

```bash
docker-compose -f dvd-rental.yml up
```

This will create an empty `mysql` instance, which you can use to start setting up databases

- verify the container is running

```bash
docker container ls -a
```

- <https://hevodata.com/learn/docker-mysql/>

## Loading `sample mysql` databases

### dvd_rental

Once, you've set up your `mysql` instance, you can load the sample `dvd_rental` database by executing the SQL commands available in `sql/dvd-rental-sample-db` folder of this repo

### sakila

### employees

### world_x

## References

- <https://pip.pypa.io/en/stable/installing/>
- <https://medium.com/employbl/how-to-install-mysql-on-mac-osx-5b266cfab3b6>
- <https://phoenixnap.com/kb/how-to-create-a-table-in-mysql>
- <https://phoenixnap.com/kb/mysql-commands-cheat-sheet>
- <https://linuxize.com/post/show-tables-in-mysql-database/>
- <https://dev.mysql.com/doc/refman/8.0/en/char.html>
