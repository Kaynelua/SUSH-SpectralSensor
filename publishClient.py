import paho.mqtt.client as mqtt
client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt",
	certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org",port=8883)

MSG_INFO = client.publish("IC.Embedded/IOS/test","hello")

print(mqtt.error_string(MSG_INFO.rc))