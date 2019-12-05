#!/usr/bin/env python

import intersectionLaneSwitches as ils
import wpManager as wpm
import requests
import time
import numpy as np

#the function (copied from Learning Suite) to get you location 
def getCoor(color):
    # api-endpoint
	URL = "http://192.168.1.8:8080/%s" % color
 
    # sending get request and saving the response as response object
	r = requests.get(url = URL)
 
    # extracting data
	coorString = r.text
	coordinates = coorString.split()
	try:
		latitude = float(coordinates[0])
		longitude = float(coordinates[1])
		return (latitude, longitude)
	except IndexError:
		print("IndexError in accessing coordinates")
		return(0,0)
	except:
		print("other errror")
		return(0,0)
