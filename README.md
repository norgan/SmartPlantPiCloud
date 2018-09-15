# SmartPlantPiCloud
The goal of this project is to provide a plant monitoring solution with temperature, humidity, light levels and soil moisture sending metrics to the cloud. The project is written in Python and can run from a Raspberry Pi. It also includes being able to take photos from the raspi camera for timelapse use. 

## This project leverages some or all of the following dependencies: 
- Cloud4RPI http://docs.cloud4rpi.io/start/rpi/ - Sends data to the cloud to be put into charts, guages etc
- GrovePi board for analogue input and grove connectors https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/
- SI1145 light sensor from adafruit https://learn.adafruit.com/adafruit-si1145-breakout-board-uv-ir-visible-sensor/downloads
- Seeed analogue moisture sensor https://www.seeedstudio.com/ or any other analogue moisture sensor. The resitive ones are easy but the cpactive ones last longer.
- Seeed sunlight sensor https://www.seeedstudio.com/ - this is not as accurate and was designed to give a UV Index figure.
- You could also use a DHT11/22 for temp and hum, this is a very easy one to use and could be added quite simply. 

We've attempted to make this as simple as possible by breaking up the sensor functions into methods. All you need to do is replace the sensor libraries and references to use any sensor. 

### Note
API Key is store in a file called config.py. A sample has been included called config.py.distro. Edit this file and enter your Cloud4RPI key then rename to config.py. 
