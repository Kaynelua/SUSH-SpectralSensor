import paho.mqtt.client as mqtt
client = mqtt.Client(transport = "websockets")
client.tls_set(certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org",port=8081)

MSG_INFO = client.publish("IC.Embedded/IOS/test","123hello")

print(mqtt.error_string(MSG_INFO.rc))