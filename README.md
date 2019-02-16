Embedded Systems Coursework 1(IOT)
==========================

Group name : IOS(Inventors Of Stuff)

Our device SUSH uses the spectral sensor provided along with a proximity sensor to automatically detect the color of each colored plate in a sushi restaurant which will be collated for instant and errorless bill generation. 
Upon detection of a colored plate, a message containing the color of the plate will be sent to the MQTT Broker which in turn will trigger a callback on the Web server subscribed to the MQTT broker. The price of each colored plate will be configured by restaurant owners/ managers beforehand and upon receiving the message containing the color of the plate detected, render the bill dynamically and instantly using reactJS.

How to run the application:

1.Setup Web application to subscribe to the MQTT Broker and listen for incoming messages sent on preset topic - From repository root directory, $cd my_app to enter application folder and then run $python3 flask_app.py and run web application on browser via local directory : "http://127.0.0.1:5000/"
2. Go back to root repository folder and run $python3 main.py to start automatic detection of plates. Upon detection of a plate, message wil be sent by device to the MQTT broker and be received on the web application to update the orders and bill in real time.
3. For simulation purposes, one can also run $python3 publishClient.py to simulate message sending which sends a random color to the MQTT broker. 

Brief Description of files:

my_app(folder) : Contains the source code for the instant bill generating application which can be found in my_app/templates/base.html and my_app/templates/index.html

data.pickle : A pickle file that contains pre-trained data for converting a tuple of 6 floating point numbers(Intensities at 6 different frequencies) to a string describing the color of the plate detected.

I2C.py : Low-level functions to read/write data from Spectral sensor using I2C interface which is used by SpectralSensor.py

I2C_prox.py : Low-level functions to read/write data from Proximity sensor using I2C interface which is used by ProximitySensor.py

SpectralSensor.py : Contains SpectralSensor class and its methods to read/write or control settings.

ProximitySensor.py : Contains ProximitySensor class and its methods to read/write or control settings.

Servo.py : Contains methods to control servomotor to open or close the gate.

Mqtt.py : Contains a class that connects to MQTT broker upon construction and sends the compressed message to the broker upon 
detection of a colored plate.

PlateDetector.py : Contains PlateDetector class which consists of other sensor classes and have functions that integrates the
whole process of training, scanning and releasing the plates and sends message from buffer via threading. 

main.py : runs main loop of the program


Misc files for debugging purposes :

keys(folder) : Contains the certificates required to communicate on ports i.e 8883 requiring certificates.

subscribeClient.py : Client subscribes to MQTT broker and uses certificates which can be used instead of our javascript application to listen and debug the messages sent by device.

publishClient.py : Client that sends a message to MQTT broker containing a random color to simulate message sending from device for purpose of debugging Application(Js).
