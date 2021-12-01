import random
from paho.mqtt import client as mqtt_client
import os
import json
import time

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Ds5EWYtKEvV3YqWkQdWd'
port = 1883

from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo


telemetry = {"temperature": 41.7, "enabled": False, "currentFirmwareVersion": "v1.2.2"}

#
# # Connect to ThingsBoard
# client.connect()
# # Sending telemetry without checking the delivery status
# client.send_telemetry(telemetry)
# # Sending telemetry and checking the delivery status (QoS = 1 by default)
# result = client.send_telemetry(telemetry)
# # get is a blocking call that awaits delivery status
# success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
# # Disconnect from ThingsBoard
# client.disconnect()


from time import sleep
from tb_device_mqtt import TBDeviceMqttClient


def callback(result):
    print(result)

client = TBDeviceMqttClient(THINGSBOARD_HOST, ACCESS_TOKEN)
client.connect()
client.subscribe_to_all_attributes(callback)
while True:
    sleep(1)
