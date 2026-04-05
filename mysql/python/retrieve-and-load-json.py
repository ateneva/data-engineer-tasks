
import json
import requests
from mysql.connector import connect, Error

# pylint: disable=C0116  # docstring
# pylint: disable=C0103  # snake_case naming of variables

def retrieve_data(link):
    response = requests.get(link)
    todos = json.loads(response.text)
    return todos


def establish_connection(ip, username, credentials, database):
    try:
        with connect(
                host=ip,
                user=username,
                password=credentials,
                database=database
        ) as connection:
            print(connection)
    except Error as err:
        print(err)


def insert_values():
    # engine = create_engine('mysql://root:ateneva2021@localhost/airflow')
    conn = connect(host='localhost', user='root', password='ateneva2021', db='airflow')
    data = retrieve_data('https://xkcd.com/info.0.json')
    to_insert = [data]
    print(type(data), data)
    print(type(to_insert), to_insert)
    print(data[0])

    insert_comics = """
                    INSERT INTO comics (month, num, link, year, news, safe_title, transcript, alt, img, title, day)
                    VALUES (%s, %s, $s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
    # VALUES (%s, %s, $s, %s, %s, %s, %s, %s, %s, %s, %s)
    # VALUES ('5', '2459', '', '2021', '', 'March 2020', '', '"Ive traveled here from the year 2020 to bring you this vaccine!"', 'https://imgs.xkcd.com/comics/march_2020.png', 'March 2020', '5')
    with conn.cursor() as cursor:
        cursor.execute(insert_comics, data)
        conn.commit()


if __name__ == '__main__':
    #retrieved = retrieve_data("https://jsonplaceholder.typicode.com/todos")
    retrieved = retrieve_data("https://xkcd.com/info.0.json")
    print(retrieved)

    establish_connection('localhost', 'root', 'ateneva', 'sakila')
    