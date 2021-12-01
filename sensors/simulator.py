import datetime
import os
import psycopg2
import time
import random

sensors = True
svobodno = True
start_value = 1000

# Параметры базы данных
DB_HOST = 'ec2-54-220-223-3.eu-west-1.compute.amazonaws.com'
DB_NAME = 'd1qh0q37f68ihu'
DB_USER = 'xuopetszbnqxgg'
DB_PASS = '127657c7503f50b2f7c54a93f1c79f2b328f6e6dac3515bf0a9d36d9ab8f07fc'

# Соединение с базой данных по нашим данным
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# Создание курсора
cur = conn.cursor()


def insert_data(place_id, state_id):
    cur.execute("INSERT INTO parking (place_id, state_id, date, time) VALUES (%s, %s, %s, %s)",
                (place_id, state_id, datetime.date.today(), time.strftime("%H:%M:%S")))
    conn.commit()

# Класс датчика
class Sensor:
    def __init__(self, id_sensor, value, state):
        self.id_sensor = id_sensor
        self.value = value
        self.state = state

    def set_value(self):
        if self.state == svobodno:
            self.value = random.randint(start_value - 25, start_value + 25)
        else:
            self.value = random.randint(start_value * 3 - 25, start_value * 3 + 25)

    def get_value(self):
        return self.value

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state


# Инициализация обьектов датчиков
sensor_1 = Sensor(1, start_value, 1)
sensor_2 = Sensor(2, start_value, 1)
sensor_3 = Sensor(3, start_value, 1)
sensor_4 = Sensor(4, start_value, 1)
sensor_5 = Sensor(5, start_value, 1)

# Обновление информации в БД
insert_data(sensor_1.id_sensor, sensor_1.get_state())
insert_data(sensor_2.id_sensor, sensor_2.get_state())
insert_data(sensor_3.id_sensor, sensor_3.get_state())
insert_data(sensor_4.id_sensor, sensor_4.get_state())
insert_data(sensor_5.id_sensor, sensor_5.get_state())

# Работа системы
while sensors:
    print('---------------------------')
    if sensor_1.state == 1 or sensor_2.state == 1 or sensor_3.state == 1 or sensor_4.state == 1 or sensor_5.state == 1:
        print('Свободные парковочные места: ')
        if sensor_1.state == 1:
            print('Парковочное место №', sensor_1.id_sensor)
            sensor_1.set_value()
        if sensor_2.state == 1:
            print('Парковочное место №', sensor_2.id_sensor)
            sensor_2.set_value()
        if sensor_3.state == 1:
            print('Парковочное место №', sensor_3.id_sensor)
            sensor_3.set_value()
        if sensor_4.state == 1:
            print('Парковочное место №', sensor_4.id_sensor)
            sensor_4.set_value()
        if sensor_5.state == 1:
            print('Парковочное место №', sensor_5.id_sensor)
            sensor_5.set_value()
    print('---------------------------')

    if sensor_1.state == 0 or sensor_2.state == 0 or sensor_3.state == 0 or sensor_4.state == 0 or sensor_5.state == 0:
        print('Занятые парковочные места: ')
        if sensor_1.state == 0:
            print('Парковочное место №', sensor_1.id_sensor)
            sensor_1.set_value()
        if sensor_2.state == 0:
            print('Парковочное место №', sensor_2.id_sensor)
            sensor_2.set_value()
        if sensor_3.state == 0:
            print('Парковочное место №', sensor_3.id_sensor)
            sensor_3.set_value()
        if sensor_4.state == 0:
            print('Парковочное место №', sensor_4.id_sensor)
            sensor_4.set_value()
        if sensor_5.state == 0:
            print('Парковочное место №', sensor_5.id_sensor)
            sensor_5.set_value()
    print('---------------------------')

    x = int(input('Если вы хотите занять свободное место, напишите номер места, если нет - 0 '))
    if x == 0:
        pass
    elif x == 1 and sensor_1.get_state() == 1:
        sensor_1.set_state(0)
        sensor_1.set_value()
        insert_data(sensor_1.id_sensor, sensor_1.get_state())
    elif x == 2 and sensor_2.get_state() == 1:
        sensor_2.set_state(0)
        sensor_2.set_value()
        insert_data(sensor_2.id_sensor, sensor_2.get_state())
    elif x == 3 and sensor_3.get_state() == 1:
        sensor_3.set_state(0)
        sensor_3.set_value()
        insert_data(sensor_3.id_sensor, sensor_3.get_state())
    elif x == 4 and sensor_4.get_state() == 1:
        sensor_4.set_state(0)
        sensor_4.set_value()
        insert_data(sensor_4.id_sensor, sensor_4.get_state())
    elif x == 5 and sensor_5.get_state() == 1:
        sensor_5.set_state(0)
        sensor_5.set_value()
        insert_data(sensor_5.id_sensor, sensor_5.get_state())
    else:
        print('Это место уже занято, попробуйте другое')

    print('---------------------------')

    # ОТЛАДКА
    print(sensor_1.value, sensor_1.state)
    print(sensor_2.value, sensor_2.state)
    print(sensor_3.value, sensor_3.state)
    print(sensor_4.value, sensor_4.state)
    print(sensor_5.value, sensor_5.state)

    cur.execute(
        "SELECT place_name, state_name, max(date), max(time) FROM parking, place, state "
        "WHERE place_id = place.id and state_id = state.id "
        "group by place_name, state_name "
        "order by place_name;")

    print(cur.fetchall())


