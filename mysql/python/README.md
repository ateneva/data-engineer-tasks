
# Loading data into a MySQL database

```bash
pip install mysqlclient
pip install mysql-connector-python
pip install pymysql
pip install sqlalchemy
```

<!-- markdownlint-disable MD007 -->

<!-- TOC -->

- [Loading data into a MySQL database](#loading-data-into-a-mysql-database)
    - [using mysql-connector](#using-mysql-connector)
        - [create databases](#create-databases)
        - [connect to a database](#connect-to-a-database)
        - [show databases](#show-databases)
        - [create a single table](#create-a-single-table)
        - [create multiple tables](#create-multiple-tables)
        - [alter table schema](#alter-table-schema)
        - [insert records](#insert-records)
        - [read records](#read-records)
        - [update records](#update-records)
        - [drop table](#drop-table)
    - [using pymysql](#using-pymysql)
    - [using sqlalchemy](#using-sqlalchemy)
        - [create engine](#create-engine)
        - [create table](#create-table)
    - [References](#references)

<!-- /TOC -->

## using mysql-connector

### create databases

```python
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "dbms"
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

## creating a databse called 'datacamp'
## 'execute()' method is used to compile a 'SQL' statement
## below statement is used to create tha 'datacamp' database
cursor.execute("CREATE DATABASE datacamp")
```

### connect to a database

```python
## Connecting to the database

## importing 'mysql.connector' as mysql for convenient
import mysql.connector as mysql

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'

print(db) # it will print a connection object if everything is fine
```

### show databases

```python
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "dbms"
)

cursor = db.cursor()

## executing the statement using 'execute()' method
cursor.execute("SHOW DATABASES")

## 'fetchall()' method fetches all the rows from the last executed statement
databases = cursor.fetchall() ## it returns a list of all databases present

## printing the list of databases
print(databases)

## showing one by one database
for database in databases:
    print(database)
```

### create a single table

```python
create_movies_table_query = """
CREATE TABLE movies(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    release_year YEAR(4),
    genre VARCHAR(100),
    collection_in_mil INT
)
"""
with connection.cursor() as cursor:
    cursor.execute(create_movies_table_query)
    connection.commit()
```

### create multiple tables

```python
create_reviewers_table_query = """
CREATE TABLE reviewers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
)
"""

create_ratings_table_query = """
CREATE TABLE ratings (
        movie_id INT,
        reviewer_id INT,
        rating DECIMAL(2,1),
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(reviewer_id) REFERENCES reviewers(id),
    PRIMARY KEY(movie_id, reviewer_id)
)
"""

with connection.cursor() as cursor:
    cursor.execute(create_movies_table_query)
    cursor.execute(create_reviewers_table_query)
    cursor.execute(create_ratings_table_query)
    connection.commit()

```

### alter table schema

```python
alter_table_query = """
    ALTER TABLE movies
     MODIFY COLUMN collection_in_mil DECIMAL(4,1)
     """

show_table_query = "DESCRIBE movies"

with connection.cursor() as cursor:
    cursor.execute(alter_table_query)
    cursor.execute(show_table_query)

# Fetch rows from last executed query
result = cursor.fetchall()
print("Movie Table Schema after alteration:")
for row in result:
    print(row)
```

### insert records

```python
insert_reviewers_query = """
INSERT INTO reviewers
(first_name, last_name)
VALUES ( %s, %s )
"""
reviewers_records = [
    ("Chaitanya", "Baweja"),
    ("Mary", "Cooper"),
    ("John", "Wayne"),
    ("Thomas", "Stoneman"),
    ("Penny", "Hofstadter"),
    ("Mitchell", "Marsh"),
    ("Wyatt", "Skaggs"),
    ("Andre", "Veiga"),
    ("Sheldon", "Cooper"),
    ("Kimbra", "Masters"),
    ("Kat", "Dennings"),
    ("Bruce", "Wayne"),
    ("Domingo", "Cortes"),
    ("Rajesh", "Koothrappali"),
    ("Ben", "Glocker"),
    ("Mahinder", "Dhoni"),
    ("Akbar", "Khan"),
    ("Howard", "Wolowitz"),
    ("Pinkie", "Petit"),
    ("Gurkaran", "Singh"),
    ("Amy", "Farah Fowler"),
    ("Marlon", "Crafford"),
]
with connection.cursor() as cursor:
    cursor.executemany(insert_reviewers_query, reviewers_records)
    connection.commit()
```

```python
insert_ratings_query = """
INSERT INTO ratings
(rating, movie_id, reviewer_id)
VALUES ( %s, %s, %s)
"""
ratings_records = [
    (6.4, 17, 5), (5.6, 19, 1), (6.3, 22, 14), (5.1, 21, 17),
    (5.0, 5, 5), (6.5, 21, 5), (8.5, 30, 13), (9.7, 6, 4),
    (8.5, 24, 12), (9.9, 14, 9), (8.7, 26, 14), (9.9, 6, 10),
    (5.1, 30, 6), (5.4, 18, 16), (6.2, 6, 20), (7.3, 21, 19),
    (8.1, 17, 18), (5.0, 7, 2), (9.8, 23, 3), (8.0, 22, 9),
    (8.5, 11, 13), (5.0, 5, 11), (5.7, 8, 2), (7.6, 25, 19),
    (5.2, 18, 15), (9.7, 13, 3), (5.8, 18, 8), (5.8, 30, 15),
    (8.4, 21, 18), (6.2, 23, 16), (7.0, 10, 18), (9.5, 30, 20),
    (8.9, 3, 19), (6.4, 12, 2), (7.8, 12, 22), (9.9, 15, 13),
    (7.5, 20, 17), (9.0, 25, 6), (8.5, 23, 2), (5.3, 30, 17),
    (6.4, 5, 10), (8.1, 5, 21), (5.7, 22, 1), (6.3, 28, 4),
    (9.8, 13, 1)
]
with connection.cursor() as cursor:
    cursor.executemany(insert_ratings_query, ratings_records)
    connection.commit()
```

```python
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "dbms",
    database = "datacamp"
)

cursor = db.cursor()

## defining the Query
query = "INSERT INTO users (name, user_name) VALUES (%s, %s)"

## storing values in a variable
values = ("Hafeez", "hafeez")

## executing the query with values
cursor.execute(query, values)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

print(cursor.rowcount, "record inserted")
```

### read records

```python
select_movies_query = """
SELECT 
    title, c
    ollection_in_mil
FROM movies
WHERE collection_in_mil > 300
ORDER BY collection_in_mil DESC
"""
with connection.cursor() as cursor:
    cursor.execute(select_movies_query)
    for movie in cursor.fetchall():
    print(movie)
```

```python
select_movies_query = """
SELECT 
    CONCAT(first_name, " ", last_name), 
    COUNT(*) as num
FROM reviewers
INNER JOIN ratings
  ON reviewers.id = ratings.reviewer_id
GROUP BY reviewer_id
ORDER BY num DESC
LIMIT 1
"""

with connection.cursor() as cursor:
    cursor.execute(select_movies_query)
    for movie in cursor.fetchall():
        print(movie)
```

### update records

```python
update_query = """
UPDATE
    reviewers
SET
    last_name = "Cooper"
WHERE
    first_name = "Amy"
"""

with connection.cursor() as cursor:
    cursor.execute(update_query)
    connection.commit()
```

### drop table

```python
drop_table_query = "DROP TABLE ratings"
with connection.cursor() as cursor:
    cursor.execute(drop_table_query)
```

## using pymysql

---

```python
import pymysql
import os
import json

# connect to MySQL
con = pymysql.connect(host = 'localhost',user = 'root',passwd = '',db = 'test')
cursor = con.cursor()

# read JSON file which is in the next parent folder
file = os.path.abspath('../../..') + "/test.json"
json_data=open(file).read()
json_obj = json.loads(json_data)

# parse json data to SQL insert
for i, item in enumerate(json_obj):
    person = item.get("person", None)
    year = item.get("year", None)
    company = item.get("company", None)

    cursor.execute("INSERT INTO testp (person, year, company) VALUES (%s, %s, %s)", (person, year, company))

con.commit()
con.close()
```

## using sqlalchemy

### create engine

```python
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')

# mysqlclient (a maintained fork of MySQL-Python)
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

# PyMySQL
engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
```

### create table

```python
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('emp', metadata,
              db.Column('Id', db.Integer()),
              db.Column('name', db.String(255), nullable=False),
              db.Column('salary', db.Float(), default=100.0),
              db.Column('active', db.Boolean(), default=True)
              )

metadata.create_all(engine) #Creates the table

### insert into table

query = db.insert(emp) 
values_list = [{'Id':'2', 'name':'ram', 'salary':80000, 'active':False},
               {'Id':'3', 'name':'ramesh', 'salary':70000, 'active':True}]
ResultProxy = connection.execute(query,values_list)
```

## References

- <https://realpython.com/python-mysql/>
- <https://www.datacamp.com/community/tutorials/mysql-python>
- <https://realpython.com/prevent-python-sql-injection/>
- <https://stackoverflow.com/questions/775296/mysql-parameterized-queries>
- <http://howisonlab.github.io/datawrangling/class_modules/11_parameterized_sql_queries/>
- <https://www.tutorialspoint.com/python_data_access/python_mysql_insert_data.htm>
- <https://www.mysqltutorial.org/python-mysql-insert>
- <https://dev.to/romainnorberg/python-avoid-sql-injection-when-using-mysqlcursor-execute-4dn0>
- <https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html>
- <https://blog.softhints.com/python-read-validate-and-import-csv-json-file-to-mysql>
- <https://www.youtube.com/watch?v=mo-FU0mGNx4>
- <https://www.educative.io/edpresso/resolving-typeerror-not-all-arguments-converted-in-python>

- <https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91>
- <https://www.pythonsheets.com/notes/python-sqlalchemy.html>
- <https://www.youtube.com/watch?v=aWN1CqMtzIE>
