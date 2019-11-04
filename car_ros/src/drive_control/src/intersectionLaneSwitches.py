#!/usr/bin/env python
import wpManager as wpm
import numpy as np


csvPath = "/home/nvidia/Desktop/class_code/self_driving_car/car_ros/src/drive_control/src/waypoints/course_1.csv"
wps = wpm.csv2WayPoint(csvPath) # the waypoints are loaded

def one():
	global wps
	print("Intersection lane 1")
	if len(wps) != 0:
		inter = wpm.reachedIntersection(wps[0])
		wps = np.delete(wps,0,0)
		if inter == 6:
			print("turn right")
			return 1
		elif inter == 7:
			print("go straight")
			return 0
		elif inter == 8:
			print("turn left")
			return -1
		else:
			print("error, in intersection 1 and I don't know where to go")
	else:
		print("Finished waypoints")
		return 2

	#direction to go depends on the location of our next waypoint

def two():
	global wps
	print("Intersection lane 2")
	if len(wps) != 0:
		inter = wpm.reachedIntersection(wps[0])
		wps = np.delete(wps,0,0)
		if inter == 7:
			print("turn right")
			return 1
		elif inter == 8:
			print("go straight")
			return 0
		elif inter == 5:
			print("turn left")
			return -1
		else:
			print("error, in intersection 1 and I don't know where to go")
	else:
		print("Finished waypoints")
		return 2
	#direction to go depends on the location of our next waypoint

def three():
	global wps
	print("Intersection lane 3")
	if len(wps) != 0:
		inter = wpm.reachedIntersection(wps[0])
		wps = np.delete(wps,0,0)
		if inter == 8:
			print("turn right")
			return 1
		elif inter == 5:
			print("go straight")
			return 0
		elif inter == 6:
			print("turn left")
			return -1
		else:
			print("error, in intersection 1 and I don't know where to go")
	else:
		print("Finished waypoints")
		return 2
	#direction to go depends on the location of our next waypoint

def four():
	global wps
	print("Intersection lane 4")
	if len(wps) != 0:
		inter = wpm.reachedIntersection(wps[0])
		wps = np.delete(wps,0,0)
		if inter == 5:
			print("turn right")
			return 1
		elif inter == 6:
			print("go straight")
			return 0
		elif inter == 7:
			print("turn left")
			return -1
		else:
			print("error, in intersection 1 and I don't know where to go")
	else:
		print("Finished waypoints")
		return 2
	#direction to go depends on the location of our next waypoint

def five():
	print("Drove into intersection lane 5")
	global wps
	if len(wps) == 0:
		return 2
	return None

def six():
	print("Drove into intersection lane 6")
	global wps
	if len(wps) == 0:
		return 2
	return None

def seven():
	print("Drove into intersection lane 7")
	global wps
	if len(wps) == 0:
		return 2
	return None

def eight():
	print("Drove into intersection lane 8")
	global wps
	if len(wps) == 0:
		return 2
	return None

def nine():
	print("Intersection lane 9")
	global wps
	if len(wps) != 0:
		wps = np.delete(wps,0,0)
		print("turn left")
		return -1
	else:
		print("error, no more waypoints")
		return 2
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn

def ten():
	print("Intersection lane 10")
	global wps
	if len(wps) != 0:
		wps = np.delete(wps,0,0)
		print("turn right") #put code to turn here
		return 1
	else:
		print("error, no more waypoints")
		return 2
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn

def eleven():
	print("Intersection lane 11")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn
	global wps
	if len(wps) != 0:
		wps = np.delete(wps,0,0)
		print("turn right")
		return 1
	else:
		print("error, no more waypoints")
		return 2

def twelve():
	print("Intersection lane 12")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn
	global wps
	if len(wps) != 0:
		wps = np.delete(wps,0,0)
		print("turn left")
		return -1
	else:
		print("error, no more waypoints")
		return 2

def noIntersection():
	print("no intersection")
	return None


def useLaneNumber(num):
	print("using lane number")
	switcher = {
		1: one,
		2: two,
		3: three,
		4: four,
		5: five,
		6: six,
		7: seven, 
		8: eight,
		9: nine,
		10: ten,
		11: eleven,
		12: twelve
	}
	#get the funciton that we need to call
	func = switcher.get(num, lambda: noIntersection)
	#execute the function
	func()
