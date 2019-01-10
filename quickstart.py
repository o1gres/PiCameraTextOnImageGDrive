#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import sys
import os
import urllib
import string
import json
import requests
import time
from neopixel import *
import argparse


from picamera import PiCamera
from picamera import Color
from time import sleep

from googleapiclient.discovery import build
from httplib2 import Http
from apiclient import discovery
from oauth2client import file, client, tools

from apiclient.discovery import build
from apiclient.http import MediaFileUpload


#FLASH
# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 70     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53




# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    applicationPath = os.path.dirname(os.path.abspath(__file__))

    store = file.Storage(applicationPath+'/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(applicationPath+'/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    now = datetime.datetime.now()
    data = str(now)

    data = data.replace(" ","--")
    data = data.replace(":","-")


    hour = data[12:14]


    camera = PiCamera()

    camera.resolution = (2592, 1944)
    camera.brightness = 55
    camera.start_preview()

    #Get information from agrumino
    try:
	in_file = open(applicationPath+"/jsonLink.txt", "r")
	link = in_file.read()
	in_file.close()
        response = urllib.urlopen(link)
	dataJson = json.loads(response.read())
	temperature = dataJson['feeds'][0]['field1']
	soil = dataJson['feeds'][0]['field5']
	imageData = str(data)[0:10]
        camera.annotate_text_size = 70
        camera.annotate_foreground = Color('black')
        camera.annotate_background = Color('white')
        camera.annotate_text = " "+imageData+" Temp: "+temperature+ " - Umidita':"+soil+ "% "
    except:
        print ("error getting json information")
	pass


    if ((hour >= 0 and hour < 10) or (hour >= 18 and hour <= 23)):
        os.system('python /home/pi/Desktop/flash/rpi_ws281x/python/examples/flashon.py')

    camera.capture(applicationPath+'/foto/image' + str(data) + '.jpg')
    camera.stop_preview()

#    if ((hour >= 0 and hour < 10) or (hour >= 18 and hour <= 23)):
    os.system('python /home/pi/Desktop/flash/rpi_ws281x/python/examples/flashoff.py')



    #upload to drive
    #service = discovery.build('drive', 'v3', http=http)
    file_metadata = {'name': 'image' + str(data) + '.jpg'}
    media = MediaFileUpload(applicationPath+'/foto/image' + str(data) + '.jpg',mimetype='image/jpeg')
    file_upload = service.files().create(body=file_metadata,media_body=media,fields='id').execute()


if __name__ == '__main__':
    main()
