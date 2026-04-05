
# SQL primers

<!-- markdownlint-disable MD007 -->

<!-- TOC -->

- [SQL primers](#sql-primers)
    - [CREATE TABLE on the installed database](#create-table-on-the-installed-database)
    - [INSERT values](#insert-values)
    - [CHECK DATABASES and TABLES](#check-databases-and-tables)
    - [MODIFY column type](#modify-column-type)
    - [SHOW users](#show-users)
    - [DATETIME FUNCTIONS](#datetime-functions)
        - [EXTRACT](#extract)
        - [DATE_ADD / DATE_SUB](#date_add--date_sub)
        - [PERIOD_ADD / PERIOD_DIF](#period_add--period_dif)
        - [DATEDIFF](#datediff)
        - [LAST DAY](#last-day)

<!-- /TOC -->

## CREATE TABLE on the installed database

```sql
CREATE TABLE movies(
    title VARCHAR(50) NOT NULL,
    genre VARCHAR(30) NOT NULL,
    director VARCHAR(60) NOT NULL,
    release_year INT NOT NULL,
    PRIMARY KEY(title)`
);
```

## INSERT values

```sql
INSERT INTO movies
VALUES ("Joker", "psychological thriller", "Todd Phillips", 2019);
```

## CHECK DATABASES and TABLES

```bash
MySQL -u root -p
SHOW DATABASES;
SHOW TABLES from database;
quit

# OR
USE database;
SHOW TABLES LIKE pattern;
SHOW TABLES;
quit
```

## MODIFY column type

```sql
ALTER TABLE table_name    
MODIFY column_name datatype;  
```

## SHOW users

```bash
MySQL -u root -p
desc mysql.user;
select user from mysql.user;
```

## DATETIME FUNCTIONS

- **STR_TO_DATE**

```sql
SELECT
    '2017-03-31'                          AS text_field,
    STR_TO_DATE('2017-03-31', '%Y-%m-%d') AS date_field
```

- **STANDARD DATE FUNCTIONS**

```sql
SELECT
    NOW(),
    DATE(CURRENT_DATE())        AS today,
    YEAR(CURRENT_DATE())        AS this_year,
    QUARTER(CURRENT_DATE())     AS this_quarter,
    MONTH(CURRENT_DATE())       AS this_month,
    DAY(CURRENT_DATE())         AS this_day,
    
    DAYOFYEAR(CURRENT_DATE())   AS day_of_year,
    DAYOFMONTH(CURRENT_DATE())  AS day_of_month,
    
    #1 = Sunday, 2 = Monday, …, 7 = Saturday)
    DAYOFWEEK(CURRENT_DATE())   AS day_of_week, 
    
    #0 = Monday, 1 = Tuesday, … 6 = Sunday  
    WEEKDAY(CURRENT_DATE())     AS weekday_num,  
    
    WEEKOFYEAR(CURRENT_DATE())  AS week_num_us,
    WEEK(CURRENT_DATE())        AS week_num_us
```

- ### **EXTRACT**

```sql
SELECT
    CURRENT_TIMESTAMP                        AS my_local_date_and_time,
    EXTRACT(YEAR FROM CURRENT_TIMESTAMP)     AS current_year,            
    EXTRACT(QUARTER FROM CURRENT_TIMESTAMP)  AS current_quarter,
    EXTRACT(month FROM CURRENT_TIMESTAMP)    AS current_month,
    EXTRACT(week FROM CURRENT_TIMESTAMP)     AS current_week,
    EXTRACT(day FROM CURRENT_TIMESTAMP)      AS current_day,
    EXTRACT(hour FROM CURRENT_TIMESTAMP)     AS current_hour
```

- ### **DATE_ADD() / DATE_SUB()**

```sql
SELECT
    DATE_ADD(NOW(), INTERVAL 1 YEAR)    AS one_year_from_now,
    DATE_ADD(NOW(), INTERVAL 1 MONTH)   AS month_from_now,
    DATE_ADD(NOW(), INTERVAL 1 WEEK)    AS one_week_from_now,
    DATE_ADD(NOW(), INTERVAL 1 DAY)     AS one_day_from_now,
    DATE_ADD(NOW(), INTERVAL 1 HOUR)    AS one_hour_from_now
```

```sql
SELECT
    DATE_ADD(NOW(), INTERVAL -1 YEAR)    AS one_year_ago,
    DATE_ADD(NOW(), INTERVAL -1 MONTH)   AS one_month_ago,
    DATE_ADD(NOW(), INTERVAL -1 WEEK)    AS one_week_ago,
    DATE_ADD(NOW(), INTERVAL -1 DAY)     AS one_day_ago,
    DATE_ADD(NOW(), INTERVAL -1 HOUR)    AS one_hour_ago
```

 or

```sql
SELECT
    DATE_SUB(NOW(), INTERVAL 1 YEAR)    AS one_year_ago,
    DATE_SUB(NOW(), INTERVAL 1 MONTH)   AS one_month_ago,
    DATE_SUB(NOW(), INTERVAL 1 WEEK)    AS one_week_ago,
    DATE_SUB(NOW(), INTERVAL 1 DAY)     AS one_day_ago,
    DATE_SUB(NOW(), INTERVAL 1 HOUR)    AS one_hour_ago
```

- ### **PERIOD_ADD / PERIOD_DIF**

```sql
# fixed input month
SELECT
    NOW(),
    PERIOD_ADD(201801, 3) AS 3_month_from_ym,
    PERIOD_ADD(201801,-3) AS 3_month_ago,

# get current year month
    CONCAT(YEAR(NOW()),  
        CASE
            WHEN MONTH(NOW()) < 10 THEN CONCAT(0, MONTH(NOW()))
            ELSE  MONTH(NOW())
        END) AS this_ym,


# dynamic input month
    PERIOD_ADD(CONCAT(YEAR(NOW()),  
                    CASE
                        WHEN MONTH(NOW()) < 10 THEN CONCAT(0, MONTH(NOW()))
                        ELSE MONTH(NOW())
                    END), 5) AS 5_months_from_now
```

- ### **DATEDIFF**

```sql
SELECT
    DATEDIFF(NOW(), '1988-06-21') AS days_between,
    DATEDIFF(YEAR,    '1988-06-21', NOW()) AS years_between_dates,
    DATEDIFF(QUARTER, '1988-06-21', NOW()) AS quarters_between_dates,
    DATEDIFF(MONTH,   '1988-06-21', NOW()) AS months_between_dates,
    DATEDIFF(DAY,     '1988-06-21', NOW()) AS days_between_dates,
    DATEDIFF(HOUR,    '1988-06-21', NOW()) AS hours_between_dates,
    DATEDIFF(MINUTE,  '1988-06-21', NOW()) AS minutes_between_dates,
    DATEDIFF(SECOND,  '1988-06-21', NOW()) AS seconds_between_dates
```

- ### **LAST DAY**

```sql
SELECT
    DATE(NOW())                   AS today,
    LAST_DAY(ADDDATE(NOW(), -31)) AS last_day_previous_month,
    LAST_DAY(NOW())               AS last_day_this_month,
    LAST_DAY(ADDDATE(Now(), +31)) AS last_day_next_month
```
