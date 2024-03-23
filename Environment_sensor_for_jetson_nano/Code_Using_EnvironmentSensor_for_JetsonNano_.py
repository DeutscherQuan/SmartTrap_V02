#!/usr/bin/python
# -*- coding:utf-8 -*-
# initial set up of imports

import time
import datetime
import BME280   #Atmospheric Pressure/Temperature and humidity
import TSL2591  #LIGHT
from PIL import Image,ImageDraw,ImageFont
import math
import csv
import ina219
import pyrebase
#import urllib3
import schedule
import signal

# Declare Firebase address to connect to Python
config = {
  "apiKey": "AIzaSyDQzoT9FMh9wVGVLrF6oT8PUIaX8gOsMlQ",
  "authDomain": "test-5b0a6.firebaseapp.com",
  "databaseURL": "https://test-5b0a6-default-rtdb.firebaseio.com",
  "projectId": "test-5b0a6",
  "storageBucket": "test-5b0a6.appspot.com",
  "messagingSenderId": "408527207975",
  "appId": "1:408527207975:web:4b51fe74fe1c82192a1802",
  "measurementId": "G-BDW2J9WDZB"
 }

firebase = pyrebase.initialize_app(config)

bme280 = BME280.BME280()
bme280.get_calib_param()
light = TSL2591.TSL2591()
light.SET_LuxInterrupt(20, 200)


try:
    # sensor.setup()
    #BME
    data_bme280 = []
    data_bme280 = bme280.readData()
    pressu = str(round(data_bme280[0], 2))
    temp = str(round(data_bme280[1], 2))
    humi = str(round(data_bme280[2], 2))

    #light(TSL2591)
    lux = light.Lux()
    ss_light = str(round(lux, 2))

    today = datetime.datetime.now()
    date_time = today.strftime("%y%m%d%H%M")
    database = firebase.database()
    if (today.minute % 15 == 0):
        database.child("Environment Sensor Storage").child("BME Storage").remove()
        print ("Deleted data!")
        signal.alarm(0)
    else:
        pass

    try:
        signal.alarm(75)	
        database = firebase.database()  
        database.child("Environment Sensor Storage").child("BME Storage").child("Temperature").push(temp)
        #time.sleep(0.5)
        database.child("Environment Sensor Storage").child("BME Storage").child("Humidity").push(humi)
        database.child("Environment Sensor Storage").child("Light Sensor").child("Illumination").push(ss_light)
        print ("Send Environmental Data to User Dashboard!")
        print ("Pressure: " + pressu + " Pa")
        print ("Temperature: " + temp + " °C")
        print ("Humidity: " + humi + " %")
        print ("Light: " + ss_light + " lux")
        print ("Datetime: " + date_time)
        signal.alarm(0)		

    except Exception as e:	
        signal.alarm(0)
        print (e)
        print ("Send data failed!")
        pass

except KeyboardInterrupt:
    pass





