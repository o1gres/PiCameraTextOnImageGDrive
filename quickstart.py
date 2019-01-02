#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import sys
import os
import urllib
import string
import json
import requests

from picamera import PiCamera
from picamera import Color
from time import sleep

from googleapiclient.discovery import build
from httplib2 import Http
from apiclient import discovery
from oauth2client import file, client, tools

from apiclient.discovery import build
from apiclient.http import MediaFileUpload



# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

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


    camera = PiCamera()

    camera.resolution = (2592, 1944)

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

    camera.capture(applicationPath+'/foto/image' + str(data) + '.jpg')
    camera.stop_preview()


    #upload to drive
    #service = discovery.build('drive', 'v3', http=http)
    file_metadata = {'name': 'image' + str(data) + '.jpg'}
    media = MediaFileUpload(applicationPath+'/foto/image' + str(data) + '.jpg',mimetype='image/jpeg')
    file_upload = service.files().create(body=file_metadata,media_body=media,fields='id').execute()



    #print 'File ID: %s' % file.get('id') 


   # Call the Drive v3 API
#    results = service.files().list(
#        pageSize=10, fields="nextPageToken, files(id, name)").execute()
#    items = results.get('files', [])
#
#    if not items:
#        print('No files found.')
#    else:
#        print('Files:')
#        for item in items:
#            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()
