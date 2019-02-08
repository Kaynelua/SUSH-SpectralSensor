import paho.mqtt.client as mqtt

MSG_INFO = client.publish("IC.Embedded/IOS/test","123hello")


class Mqtt():

	def __init__(self):
		self.client = mqtt.Client(transport = "websockets")
		self.client.tls_set(certfile="client.crt",keyfile="client.key")
		self.client.on_connect = self.on_connect
		self.client.connect("test.mosquitto.org",port=8081)

	def on_connect(self,client, userdata, flags, rc):
   		print("Succesful with result code "+str(rc))
    	# Subscribing in on_connect() means that if we lose the connection and
    	# reconnect then subscriptions will be renewed.
    	self.client.subscribe("IC.Embedded/IOS/#")
    	print(mqtt.error_string(MSG_INFO.rc))

	def send(self,topic,payload):
		MSG_INFO = self.client.publish(topic,payload)   	