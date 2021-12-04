import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('sensors/#')
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
