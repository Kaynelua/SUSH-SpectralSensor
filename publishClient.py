import paho.mqtt.client as mqtt
client = mqtt.Client(transport = "websockets")
client.tls_set(certfile="keys/client.crt",keyfile="keys/client.key")
client.connect("test.mosquitto.org",port=8081)

import random
num = random.random()
print (num)

if(num <0.5):
	MSG_INFO = client.publish("IC.Embedded/IOS/test","blue")
else:
	MSG_INFO = client.publish("IC.Embedded/IOS/test","red")

print(mqtt.error_string(MSG_INFO.rc))