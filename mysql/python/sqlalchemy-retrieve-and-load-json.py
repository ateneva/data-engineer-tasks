
""" functions to retrieve data with sql alchemy """
from datetime import datetime
import time
import json
import requests
import sqlalchemy as db


today = datetime.today().strftime('%Y-%m-%d')

engine = db.create_engine('mysql+pymysql://root:ateneva2021@localhost/airflow')
connection = engine.connect()
metadata = db.MetaData()

# pylint: disable=C0116  # docstring
# pylint: disable=C0103  # snake_case naming of variables

def create_table():
    xkcd_comics = db.Table('xkcd_comics', metadata,
                            db.Column('month', db.String(2), nullable=False),
                            db.Column('num', db.Integer(), nullable=False),
                            db.Column('link', db.String(1000), nullable=False),
                            db.Column('year', db.String(4), nullable=False),
                            db.Column('news', db.String(1000), nullable=False),
                            db.Column('safe_title', db.String(1000), nullable=False),
                            db.Column('transcript', db.String(5000), nullable=False),
                            db.Column('alt', db.String(5000), nullable=False),
                            db.Column('img', db.String(600), nullable=False),
                            db.Column('title', db.String(1000), nullable=False),
                            db.Column('day', db.String(2), nullable=False)
                            )
    metadata.create_all(engine)
    return f'Created {xkcd_comics} table'


def retrieve_data(link):
    response = requests.get(link)
    daily_comics = [json.loads(response.text)]
    return daily_comics


def new_data(daily_comics):
    today_date = datetime(int(daily_comics[0]['year']), int(daily_comics[0]['month']),
                          int(daily_comics[0]['day'])).strftime('%Y-%m-%d')
    if today_date == today:
        return True
    return False


def insert_values(backfill=False):
    comics_data = db.Table('xkcd_comics', metadata, autoload=True, autoload_with=engine)
    query = db.insert(comics_data)

    # retrieve the the range of already inserted comic_id
    select_latest = db.select([db.func.max(comics_data.columns.num)])
    select_first = db.select([db.func.min(comics_data.columns.num)])
    max_comic_id = connection.execute(select_latest).scalar()
    min_comic_id = connection.execute(select_first).scalar()
    print(min_comic_id, max_comic_id)

    link = ''
    num_inserted = 0
    if backfill:
        for i in range(max_comic_id - 180, max_comic_id):
            if i < min_comic_id:  # double check record is not already in
                link = f'https://xkcd.com/{i}/info.0.json'
                data = retrieve_data(link)
                ResultProxy = connection.execute(query, data)
                num_inserted += 1
        return f'{num_inserted} records backfilled'

    link = 'https://xkcd.com/info.0.json'
    data = retrieve_data(link)
    if max_comic_id is None:
        ResultProxy = connection.execute(query, data)
    else:
        # check that the current comic_id is not already in
        if max_comic_id < data[0]['num']:
            ResultProxy = connection.execute(query, data)

    num_inserted += 1
    return f'{num_inserted} records inserted'


def poll():
    while True:
        if new_data(retrieve_data('https://xkcd.com/info.0.json')):
            insert_values(backfill=False)
            break
        else:
            time.sleep(1800)
            return 'Re-trying in 30 minutes'


if __name__ == '__main__':
    print(create_table())
    today_data = retrieve_data('https://xkcd.com/info.0.json')
    print(today_data)
    print(today_data[0]['num'])
    print(insert_values(backfill=False))