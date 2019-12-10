#!/usr/bin/env python
import wpManager as wpm
import numpy as np


csvPath = "/home/nvidia/Desktop/class_code/self_driving_car/car_ros/src/drive_control/src/waypoints/course_3.csv"
wps = wpm.csv2WayPoint(csvPath) # the waypoints are loaded
prevInter = None

#returns:
# -1 turn left
# 1 turn right stop light
# 0 go straight
# 2 stop
# 40 turn right, stop sign
# -40 turn left, stop sign
def one():
	global wps
	#print("Intersection lane 1")
	if len(wps) != 0:

		#this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 1:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter == 2:
			print("turn right")
			return 1
		elif nextInter == 3:
			print("go straight")
			return 0
		elif nextInter == 4:
			print("turn left")
			return -1
		#elif nextInter == 1:
		#	print("deleting waypoint")
		#	wps = np.delete(wps, 0, 0)
		#	print("new wp size: ", len(wps))
		#	return None
		else:
			print("in intersection 1 and continuing")
	else:
		print("Finished waypoints")
		return 2

	#direction to go depends on the location of our next waypoint

def two():
	global wps
	#print("Intersection lane 2")
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 2:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter == 3:
			print("turn right")
			return 1
		elif nextInter == 4:
			print("go straight")
			return 0
		elif nextInter == 1:
			print("turn left")
			return -1
		#elif nextInter == 2:
		#	print("deleting waypoint")
		#	wps = np.delete(wps, 0, 0)
		#	print("new wp size: ", len(wps))
		#	return None
		else:
			print("in intersection 2 and continuing")
	else:
		print("Finished waypoints")
		return 2
	#direction to go depends on the location of our next waypoint

def three():
	global wps
	#print("Intersection lane 3")
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 3:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter == 4:
			print("turn right")
			return 1
		elif nextInter == 1:
			print("go straight")
			return 0
		elif nextInter == 2:
			print("turn left")
			return -1
		#elif nextInter == 3:
		#	#print("deleting waypoint")
		#	wps = np.delete(wps, 0, 0)
		#	#print("new wp size: ", len(wps))
		#	return None
		else:
			print("in intersection 3 and continuing")
	else:
		print("Finished waypoints")
		return 2
	#direction to go depends on the location of our next waypoint

def four():
	global wps
	#print("Intersection lane 4")
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 4:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter == 1:
			print("turn right")
			return 1
		elif nextInter == 2:
			print("go straight")
			return 0
		elif nextInter == 3:
			print("turn left")
			return -1
		#elif nextInter == 4:
		#	#print("deleting waypoint")
		#	wps = np.delete(wps, 0, 0)
		#	#print("new wp size: ", len(wps))
		#	return None
		else:
			print("in intersection 4 and continuing")
			return None
	else:
		print("Finished waypoints")
		return 2
	#direction to go depends on the location of our next waypoint

def five():
	#print("Intersection lane 5")
	global wps
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 5:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		#if nextInter == 5:
		#	wps = np.delete(wps,0,0)
		#	#print("new wp size: ", len(wps))
		#	return None
		if nextInter == 6:
			print("turn left stop sign")
			return -40
		else:
			print("in intersection 5 and continuing")
			return None
	else:
		print("no more waypoints")
		return 2
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn

def six():
	#print("Intersection lane 6")
	global wps
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 6:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		#if nextInter == 6:
		#	wps = np.delete(wps,0,0)
		#	print("new wp size: ", len(wps))
		#	return None
		if nextInter == 5:
			print("turn right stop sign")
			return 40
		else:
			print("in intersection 6 and continuing")
			return None
	else:
		print("no more waypoints")
		return 2
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn

def seven():
	#print("Intersection lane 7")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn
	global wps
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 7:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		#if nextInter == 7:
		#	wps = np.delete(wps,0,0)
		#	print("new wp size: ", len(wps))
		#	return None
		if nextInter == 8:
			print("turn right stop sign")
			return 40
		else:
			print("in intersection 7 and continuing")
			return None
	else:
		print("no more waypoints")
		return 2

def eight():
	#print("Intersection lane 8")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn
	global wps
	if len(wps) != 0:

		# this is to make sure that we have a valid gps point
		nextInter = wpm.reachedWarningIntersection(wps[0])
		if nextInter is not 8:
			return None
		wps = np.delete(wps, 0, 0)

		nextInter = wpm.reachedWarningIntersection(wps[0])
		#if nextInter == 8:
		#	wps = np.delete(wps,0,0)
		#	print("new wp size: ", len(wps))
		#	return None
		if nextInter == 7:
			print("turn left stop sign")
			return -40
		else:
			print("in intersection 8 and continuing")
			return None
	else:
		print("no more waypoints")
		return 2

def nine():
	if prevInter == 8:
		return 40

def noIntersection():
	print("no intersection")
	return None


def useLaneNumber(num,prevIntersect):
	global prevInter
	prevInter = prevIntersect
	#print("ILS: using lane number")
	switcher = {
		1: one,
		2: two,
		3: three,
		4: four,
		5: five,
		6: six,
		7: seven, 
		8: eight,
		9: nine
	}
	#get the funciton that we need to call
	func = switcher.get(num, lambda: noIntersection)
	#execute the function
	return func()
