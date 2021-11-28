import random
from paho.mqtt import client as mqtt_client
import os
import json
import time

# Работа датчиков
smart_sensors = True
# Стартовое значение параметров на датчиках
start_value = 1000

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Ds5EWYtKEvV3YqWkQdWd'
port = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_publish(client, userdata, result):
    print("Data from sensor published to ThingsBoard\n")
    pass

client = mqtt_client.Client("Parking_sensor_1")
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, port, keepalive=60)

client.loop_start()
while smart_sensors:
    params = random.randint(start_value - 100, start_value + 100)
    data = "{\"parameter\":" + str(params) + "}"
    client.publish("v1/devices/me/telemetry", data)
    time.sleep(5)
client.loop_stop()
client.disconnect()

# def simulation(x):
#     if x == 1:
#         while smart_sensors:
#             params = random.randint(start_value - 100, start_value + 100)
#             data = "{\"parameter\":", params, "}"
#             client.publish("v1/devices/me/telemetry", data)
#             time.sleep(5)
#     elif x == 0:
#         while smart_sensors:
#             params = random.randint(start_value * 3, start_value * 4)
#             data = "{\"parameter\":", params, "}"
#             client.publish("v1/devices/me/telemetry", data)
#             time.sleep(5)

