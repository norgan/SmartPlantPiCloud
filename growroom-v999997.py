#!/usr/bin/env python
#
# GrovePi Project for a Plant monitoring project.
#	*	Reads the data from moisture, light, temperature and humidity sensor
#		and takes pictures from the Pi camera periodically and logs them
#	*	Sensor Connections on the GrovePi:
#			-> Grove Moisture sensor	- Port A0
#			-> Grove light sensor		- I2C-1
#			-> Grove Temp sensor 		- I2C-2


import time
import grovepi
import subprocess
import math
import smbus
import SI1145

# Cloud4rpi
from time import sleep
import sys
import random
import cloud4rpi
import rpi


# analog sensor port number
mositure_sensor = 1


# Get I2C bus
bus = smbus.SMBus(1)

sensor = SI1145.SI1145()

DEVICE_TOKEN = 'AH1yEtV2hXzGPJSneShYQA85m'

# Constants
# LED_PIN = 12
DATA_SENDING_INTERVAL = 30  # secs
DIAG_SENDING_INTERVAL = 60  # secs
POLL_INTERVAL = 0.5  # 500 ms

#############
# test timings
time_for_sensor = 4  # 4 seconds
time_for_picture = 12  # 12 seconds

#	final
# time_for_sensor		= 1*60*60	#1hr
# time_for_picture		= 8*60*60	#8hr

time_to_sleep = 1
log_file = "plant_monitor_log.csv"


def readMoisture():
    try:
        moisture = grovepi.analogRead(mositure_sensor)
        print"Moisture: ", moisture
        return moisture
    except:
        print "Error in moisture reading..."
        return -1


def readUV():
    try:
        uv = sensor.readUV()
        print "UV Light: ", uv
        return uv
    except:
        print "Error in UV reading..."
        return -1


def readVisible():
    try:
        vis = sensor.readVisible()
        print "Visible Light: ", vis
        return vis
    except:
        print "Error in Light Visible reading..."
        return -1


def readIR():
    try:
        ir = sensor.readIR()
        print "Visible Light: ", ir
        return ir
    except:
        print "Error in IR reading..."
        return -1


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

# Take a picture with the current time using the Raspberry Pi camera. Save it in the same folder


def take_picture():
    try:
        cmd = "raspistill -t 1 -o plant_monitor_" + \
            str(time.strftime("%Y_%m_%d__%H_%M_%S"))+".jpg"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        process.communicate()[0]
        print("Picture taken\n------------>\n")
    except:
        print("Camera problem,please check the camera connections and settings")


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
        "Soil Moisture": {
            "type": "numeric",
            "bind": readMoisture
        }
    }

    diagnostics = {
        'CPU Temp': rpi.cpu_temp,
        'IP Address': rpi.ip_address,
        'Host': rpi.host_name,
        'Operating System': rpi.os_name
    }

    device = cloud4rpi.connect(DEVICE_TOKEN)
    device.declare(variables)
    device.declare_diag(diagnostics)
    device.publish_config()

    while True:
        curr_time_sec = int(time.time())

        # If it is time to take the sensor reading
        if curr_time_sec-last_read_sensor > time_for_sensor:

            device.publish_data()

            # Update the last read time
            last_read_sensor = curr_time_sec

        # If it is time to take the picture
        if curr_time_sec-last_pic_time > time_for_picture:
            take_picture()
            last_pic_time = curr_time_sec
            device.publish_diag()

        # Slow down the loop
        time.sleep(time_to_sleep)


if __name__ == '__main__':
    main()
