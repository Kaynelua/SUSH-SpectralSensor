#Generate a message containing random color to simulate message sending from device for purpose of debugging Application(Js)

import paho.mqtt.client as mqtt
client = mqtt.Client(transport = "websockets")
client.tls_set(certfile="keys/client.crt",keyfile="keys/client.key")
client.connect("test.mosquitto.org",port=8081)

import random
num = random.random()
print (num)


if(num <0.2):
	print("Blue")
	MSG_INFO = client.publish("IC.Embedded/IOS/test","Blue")
elif(num<0.4):
	print("Red")
	MSG_INFO = client.publish("IC.Embedded/IOS/test","Red")
elif(num<0.6):
	print("Orange")
	MSG_INFO = client.publish("IC.Embedded/IOS/test","Orange")
elif(num<0.8):
	print("White")
	MSG_INFO = client.publish("IC.Embedded/IOS/test","White")
else:
	print("Pink")
	MSG_INFO = client.publish("IC.Embedded/IOS/test","Pink")

print(mqtt.error_string(MSG_INFO.rc))
