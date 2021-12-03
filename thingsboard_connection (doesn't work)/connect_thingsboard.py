from paho.mqtt import client as mqtt_client
import time

# Работа датчиков
smart_sensors = True
working = True

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Ds5EWYtKEvV3YqWkQdWd'
port = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    data = msg.payload.decode()
    if int(data[38:42]) > 2000:
        print("MESTO ZANYATO")
    else:
        print("MESTO SVOBODNO")


client = mqtt_client.Client('Client')
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)

client.connect(THINGSBOARD_HOST, port)
print('Connected to ThingsBoard', THINGSBOARD_HOST)
time.sleep(1)


def get_data():
    while smart_sensors:
        client.loop_start()
        client.subscribe('v1/devices/me/rpc/request/+')
        time.sleep(5)
        client.loop_stop()


get_data()