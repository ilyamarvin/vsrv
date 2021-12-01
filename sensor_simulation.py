import random
from paho.mqtt import client as mqtt_client
import os
import json
import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

# Работа датчиков
smart_sensors = True
working = True
# Стартовое значение параметров на датчиках
start_value = 1000

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Ds5EWYtKEvV3YqWkQdWd'
port = 1883


class Sensor:
    def __init__(self, id_sensor, params):
        self.id_sensor = id_sensor
        self.params = params


sensors = {
    'sensor_1': Sensor(1, start_value),
    'sensor_2': Sensor(2, start_value),
    'sensor_3': Sensor(3, start_value),
    'sensor_4': Sensor(4, start_value),
}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_publish(client, userdata, result):
    print("Data from sensor published to ThingsBoard\n")
    pass


client = mqtt_client.Client('Client')
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(ACCESS_TOKEN)

client.connect(THINGSBOARD_HOST, port)
print('Connected to ThingsBoard', THINGSBOARD_HOST)
time.sleep(1)


def simulation(x):
    if x == 1:
        while smart_sensors:
            client.loop_start()
            params = random.randint(start_value - 25, start_value + 25)
            data = "{\"value\":" + str(params) + "}"
            client.publish("v1/devices/me/telemetry", data)
            time.sleep(5)
            client.loop_stop()
    elif x == 0:
        while smart_sensors:
            client.loop_start()
            params = random.randint(start_value*3-25, start_value*3+25)
            data = "{\"value\":" + str(params) + "}"
            client.publish("v1/devices/me/telemetry", data)
            time.sleep(5)
            client.loop_stop()


simulation(0)

# while working:
#     if sensors.get('sensor_1').params < 2000 or sensors.get('sensor_2').params or sensors.get('sensor_3').params or sensors.get('sensor_2').params:
#         print('Свободные парковочные места: ')
#         if sensors.get('sensor_1').params < 2000:
#             print('Место №', sensors.get('sensor_1').id_sensor)
#         if sensors.get('sensor_2').params < 2000:
#             print('Место №', sensors.get('sensor_2').id_sensor)
#         if sensors.get('sensor_3').params < 2000:
#             print('Место №', sensors.get('sensor_3').id_sensor)
#         if sensors.get('sensor_4').params < 2000:
#             print('Место №', sensors.get('sensor_4').id_sensor)
#     break


# def empty_parking_slots():
#     while smart_sensors:
#         params1 = random.randint(start_value - 25, start_value + 25)
#         params2 = random.randint(start_value - 25, start_value + 25)
#         params3 = random.randint(start_value - 25, start_value + 25)
#         params4 = random.randint(start_value - 25, start_value + 25)
#         telemetry = {list(sensors.keys())[0]: params1, list(sensors.keys())[1]: params2,
#                      list(sensors.keys())[2]: params3, list(sensors.keys())[3]: params4}
#         client = TBDeviceMqttClient(THINGSBOARD_HOST, ACCESS_TOKEN)
#         # Connect to ThingsBoard
#         client.connect()
#         # Sending telemetry without checking the delivery status
#         client.send_attributes(telemetry)
#         # Sending telemetry and checking the delivery status (QoS = 1 by default)
#         result = client.send_attributes(telemetry)
#         # get is a blocking call that awaits delivery status
#         success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
#         # Disconnect from ThingsBoard
#         client.disconnect()
#
#
# empty_parking_slots()