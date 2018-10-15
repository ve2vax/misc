#!/usr/bin/env python
# Example of  MQTT to send   BME280 sensor to mydevices widget , 
import cayenne.client
import time

import smbus2
import bme280

# Cayenne authentication info. This should be obtained from the Cayenne Das
hboard.
MQTT_USERNAME  = "xxxxxxx-xxxxx-xxxxx"
MQTT_PASSWORD  = "xxxxxxx-xxxxx-xxxxxx"
MQTT_CLIENT_ID = "xxxxx-xxxxxxx-xxxxxxx"

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)

i=0
timestamp = 0
port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address)

# the compensated_reading class has the following attributes
#print(data.id)
#print(data.timestamp)
#print(data.temperature)
#print(data.pressure)
#print(data.humidity)
vacuum = abs((data.pressure * 0.02953) - 29.53)
#print(vacuum)
temp = data.temperature

while True:
    client.loop()

    if (time.time() > timestamp + 10):
        data = bme280.sample(bus, address)
        vacuum = abs((data.pressure * 0.02953) - 29.53)
        temp = data.temperature
        client.celsiusWrite(1, temp)
        client.humidityWrite(2, data.humidity)
        client.vacuumWrite(3, vacuum)
        timestamp = time.time()
