#!/usr/bin/env python
#
#     GrovePi Project for a Plant monitoring project.
#	*	Reads the data from moisture, light, temperature and humidity sensors
#		and takes pictures from the Pi camera periodically and logs them
#	*	Sensor Connections on the GrovePi:
#			-> Grove Moisture sensor	- Port A0
#			-> Grove light sensor		- I2C-1
#			-> Grove Temp sensor 		- I2C-2


import time
import datetime
import subprocess
import math
import sys
import random
import os
import configparser
from picamera import PiCamera

#get config
config = configparser.ConfigParser()
#set the path of your config file here
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.py'))

# GrovePI Library
import grovepi

# I2C bus library
import smbus

# I2C Sensors
import SI1145

# Cloud4rpi
from time import sleep
import cloud4rpi

#Raspi metrics like CPU etc
import rpi


# analog sensor port number - set this to the analogue port on the grovepi that has your moisture sensor/s 0=1 and 1=2 etc
mositure_sensor1 = 1
mositure_sensor2 = 2

# Get I2C bus
bus = smbus.SMBus(1)

#set sensor variable for the SL1145
sensor = SI1145.SI1145()

#open the camera
camera = PiCamera()

#Cloud4RPI auth Token
DEVICE_TOKEN = config['DEFAULT']['DEVICE_TOKEN']

# Constants

DATA_SENDING_INTERVAL = 15  # secs
DIAG_SENDING_INTERVAL = 60  # secs
POLL_INTERVAL = 0.5  # 500 ms

#Timings#

# test timings
time_for_sensor = 15  # in seconds
time_for_picture = 30  # in seconds

#	final uncomment for more production ready timing values
# time_for_sensor		= 1*60*60	#1hr
# time_for_picture		= 8*60*60	#8hr

time_to_sleep = 10

# Set Log file name
log_file = "plant_monitor_log.csv"

# Function to read analogue moisture sensor 1
def readMoisture1():
    try:
        moisture1 = grovepi.analogRead(mositure_sensor1)
        print"Moisture1: ", moisture1
        return moisture1
    except:
        print "Error in moisture reading..."
        return -1

#Function to read analogue moisture sensor 2 - Comment or remove these lines if you only want one or duplicate to add additional
def readMoisture2():
    try:
        moisture2 = grovepi.analogRead(mositure_sensor2)
        print"Moisture2: ", moisture2
        return moisture2
    except:
        print "Error in moisture reading..."
        return -1

# Function to read UV light from the Grove Sunlight Sensor
def readUV():
    try:
        uv = sensor.readUV()
        print "UV Light: ", uv
        return uv
    except:
        print "Error in UV reading..."
        return -1

# Function to read visible light from the Grove Sunlight Sensor
def readVisible():
    try:
        vis = sensor.readVisible()
        print "Visible Light: ", vis
        return vis
    except:
        print "Error in Light Visible reading..."
        return -1

# Function to read IR light from the Grove Sunlight Sensor
def readIR():
    try:
        ir = sensor.readIR()
        print "Visible Light: ", ir
        return ir
    except:
        print "Error in IR reading..."
        return -1

# Function to read temperature from the Grove temp sensor
def readTemperature():
    try:
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])

        time.sleep(0.5)

        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        ctemp = round((-45 + (175 * temp / 65535.0)), 2)
        print "Temperature: ", ctemp
        return ctemp
    except:
        print "Error in temperature reading..."
        return -1

# Function to read humidity from the Grove temp sensor
def readHumidity():
    try:
        bus.write_i2c_block_data(0x44, 0x2C, [0x06])

        time.sleep(0.5)

        data = bus.read_i2c_block_data(0x44, 0x00, 6)

        # Convert the data
        humidity = round((100 * (data[3] * 256 + data[4]) / 65535.0), 2)
        print "Humidity: ", humidity
        return humidity
    except:
        print "Error in humidity reading..."
        return -1
		
# Function to read full spectrum light reading from the Grove TSL2561 sensor
def readFullLight():
	try:
		# TSL2561 address, 0x39(57)
		# Select control register, 0x00(00) with command register, 0x80(128)
		#		0x03(03)	Power ON mode
		bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)

		time.sleep(0.5)

		# Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
		# ch0 LSB, ch0 MSB
		data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

		# Convert the data
		light = data[1] * 256 + data[0]

		# Output data to screen
		print "Full Spectrum(IR + Visible) :%d lux" %light
		return light
	except:
		print "Error in light reading..."
        return -1
	
# Function to read infrared light reading from the Grove TSL2561 sensor	
def readIRLight():
	try:
		# TSL2561 address, 0x39(57)
		# Select timing register, 0x01(01) with command register, 0x80(128)
		#		0x02(02)	Nominal integration time = 402ms
		bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

		time.sleep(0.5)

		# Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
		# ch1 LSB, ch1 MSB
		data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

		# Convert the data
		irlight = data1[1] * 256 + data1[0]
		
		# Output data to screen
		print "Infrared Value :%d lux" %irlight
		return irlight
	except:
		print "Error in light reading..."
        return -1

# Take a picture with the current time using the Raspberry Pi camera. Save it in the same folder
def take_picture():
    #try:
        #cmd = "raspistill -t 1 -o os.path.dirname(__file__)/photos/plant_monitor_" + \
        #    str(time.strftime("%Y_%m_%d__%H_%M_%S"))+".jpg"
        #process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        #process.communicate()[0]
        #print("Picture taken\n------------>\n")
    #except:
        #print("Camera problem,please check the camera connections and settings")
	camera.resolution = (1024, 768)
	camera.start_preview()
	# Camera warm-up time
	sleep(2)
	date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
	camera.capture("photos/Plant"+ date +".jpg")
	print('Captured Image')
	camera.stop_preview

# Main Program
def main():
    # Save the initial time, we will use this to find out when it is time to take a picture or save a reading
    last_read_sensor = last_pic_time = int(time.time())

    # Send to Cloud4rpi using library
    # Put variable declarations here
    # Available types: 'bool', 'numeric', 'string'
    variables = {
        "Room Temp": {
            "type": "numeric",
            "bind": readTemperature
        },
        'Humidity': {
            "type": "numeric",
            "bind": readHumidity
        },
        "InfraRed Light": {
            "type": "numeric",
            "bind": readIR
        },
        "Visible Light": {
            "type": "numeric",
            "bind": readVisible
        },
        "UV Light": {
            "type": "numeric",
            "bind": readUV
        },
        "Soil Moisture1": {
            "type": "numeric",
            "bind": readMoisture1
        },
        "Soil Moisture2": {
            "type": "numeric",
            "bind": readMoisture2
        },
		"Full Spectrum Light": {
            "type": "numeric",
            "bind": readFullLight
        },
		"Ifra-Red Light": {
            "type": "numeric",
            "bind": readIRLight
        }
    }

# Send diagnostic data to Cloud4RPI
    diagnostics = {
        'CPU Temp': rpi.cpu_temp,
        'IP Address': rpi.ip_address,
        'Host': rpi.host_name,
        'Operating System': rpi.os_name
    }

# Cloud4RPI functions
    device = cloud4rpi.connect(DEVICE_TOKEN)
    device.declare(variables)
    device.declare_diag(diagnostics)
    device.publish_config()

    while True:
        curr_time_sec = int(time.time())

        # If it is time to take the sensor reading - based on time set at the top
        if curr_time_sec-last_read_sensor > time_for_sensor:

            device.publish_data()

            # Update the last read time
            last_read_sensor = curr_time_sec

        # If it is time to take the picture - based on time set at the top
        if curr_time_sec-last_pic_time > time_for_picture:
            take_picture()
            last_pic_time = curr_time_sec
            device.publish_diag()

        # Slow down the loop
        time.sleep(time_to_sleep)


if __name__ == '__main__':
    main()

