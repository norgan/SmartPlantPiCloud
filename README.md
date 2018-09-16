# SmartPlantPiCloud
The goal of this project is to provide a plant monitoring solution with temperature, humidity, light levels and soil moisture sending metrics to the cloud. The project is written in Python and can run from a Raspberry Pi. It also includes being able to take photos from the raspi camera for timelapse use. 

## This project leverages some or all of the following dependencies: 
- [Cloud4RPI](http://docs.cloud4rpi.io/start/rpi/) - Sends data to the cloud to be put into charts, guages etc, ensure you install it and its dependencies http://docs.cloud4rpi.io/faq/
- [GrovePi](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/) board for analogue input and grove connectors 
- [SI1145 light sensor from adafruit](https://learn.adafruit.com/adafruit-si1145-breakout-board-uv-ir-visible-sensor/downloads) 
- [Seeed analogue moisture sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/) or any other analogue moisture sensor. The resitive ones are easy but the cpactive ones last longer.
- [Seeed sunlight sensor](http://wiki.seeedstudio.com/Grove-Sunlight_Sensor/)- this is not as accurate and was designed to give a UV Index figure.
- You could also use a [DHT11/22](http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/) for temp and hum, this is a very easy one to use and could be added quite simply. 

We've attempted to make this as simple as possible by breaking up the sensor functions into methods. All you need to do is replace the sensor libraries and references to use any sensor. 

## Included Libraries
- Python_SI1145
- ADAFruit PureIO
- I2C
- Cloud4RPI

You may need to install some of these before the script will work. Check the links above to find out how to do that.

## Setup and configuration
- API Key is store in a file called config.py. A sample has been included called config.py.distro. Edit this file and enter your Cloud4RPI key then rename to config.py. 
- Add the python script as a service using the cloud4rpi install_service script. 
- Be sure to remark out the sensor stuff you're not using
