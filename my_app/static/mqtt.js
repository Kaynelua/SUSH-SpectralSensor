var host = "test.mosquitto.org";
var port = 8081
var topic = "IC.Embedded/IOS/#"

// Client Instance
var client = new Paho.MQTT.Client(host,port,"Main")
client.onMessageArrived = onMessageArrived;
client.onConnectionLost = onConnectionLost;

// Callback handler
client.connect({onSuccess:onConnect,
				useSSL	 :true
			   })

function onConnect() {
  console.log("Connection Succesful");
  client.subscribe(topic)
  //let message = new Paho.MQTT.Message("Hello");
  //message.destinationName = topic;
  //client.send(message);
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
}




