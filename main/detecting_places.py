import datetime
import time
import paho.mqtt.client as mqtt
import psycopg2


# Параметры базы данных
DB_HOST = 'ec2-54-220-223-3.eu-west-1.compute.amazonaws.com'
DB_NAME = 'd1qh0q37f68ihu'
DB_USER = 'xuopetszbnqxgg'
DB_PASS = '127657c7503f50b2f7c54a93f1c79f2b328f6e6dac3515bf0a9d36d9ab8f07fc'

# Соединение с нашим брокером
client = mqtt.Client()
client.connect('localhost', 1883)

# Соединение с базой данных по нашим данным
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# Создание курсора
cur = conn.cursor()

# Данные с датчиков
sensors = {
    'sensor_1': 1000,
    'sensor_2': 1000,
    'sensor_3': 1000,
    'sensor_4': 1000,
    'sensor_5': 1000
}


def sending_data():
    print(sensors)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('sensors/#')
        for i in sensors:
            cur.execute("INSERT INTO parking (place_id, state_id, date, time) VALUES (%s, %s, %s, %s)",
                        (i, 1, datetime.date.today(), time.strftime("%H:%M:%S")))
            conn.commit()
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    for i in range(5):
        if msg.topic == f'sensors/{list(sensors.keys())[i]}':
            sensors[list(sensors.keys())[i]] = int(msg.payload.decode())
            cur.execute("WITH a AS(SELECT place_id, max(id) AS msx FROM parking GROUP BY place_id) "
                        "SELECT place.place_name, state.state_name, parking.date, parking.time "
                        "FROM parking INNER JOIN place on parking.place_id=place.id "
                        "INNER JOIN state ON parking.state_id=state.id "
                        "INNER JOIN a ON parking.id=a.msx "
                        "ORDER BY place_name")
            cur.fetchall()


while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
