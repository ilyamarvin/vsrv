import datetime
import os
import psycopg2
import time
import random

# Параметры базы данных
DB_HOST = 'ec2-54-220-223-3.eu-west-1.compute.amazonaws.com'
DB_NAME = 'd1qh0q37f68ihu'
DB_USER = 'xuopetszbnqxgg'
DB_PASS = '127657c7503f50b2f7c54a93f1c79f2b328f6e6dac3515bf0a9d36d9ab8f07fc'

# Соединение с базой данных по нашим данным
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# Создание курсора
cur = conn.cursor()

x = random.randint(0, 1)
print(x)

if x == 1:
    cur.execute("INSERT INTO parking (place_id, state_id, date, time) VALUES (%s, %s, %s, %s)",
                (4, 0, datetime.date.today(), time.strftime("%H:%M:%S")))
    conn.commit()

cur.execute(
    "SELECT place_name, state_name, max(date), max(time) FROM parking, place, state "
    "WHERE place_id = place.id and state_id = state.id "
    "group by place_name, state_name "
    "order by place_name;")

print(cur.fetchall())
