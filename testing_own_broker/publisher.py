import paho.mqtt.client as mqtt
import random

start_value = 1000

client = mqtt.Client()
client.connect('localhost', 1883)


while True:
    value = random.randint(start_value - 25, start_value + 25)
    x = input('Вы хотите опубликовать сообщение? ')
    if x == '1':
        client.publish("sensors/sensor_1", value)
    else:
        break

