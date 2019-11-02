#!/usr/bin/env python
import wpManager as wpm

import numpy as np


#set up a queue of way points to use
inter5 = [317, 852]
inter6 = [567, 903]
inter7 = [625, 627]
inter8 = [365, 591]
wayPoints = np.array([inter5, inter6])

bacon = 0


def one():
	print("Intersection lane 1")
	#direction to go depends on the location of our next waypoint
	if(wpm.reachedIntersection(wayPoints[0]) == 5):
		print("Next intersection is 5, which is where we are, turn right to go in a circle")
		return 1
	elif(wpm.reachedIntersection(wayPoints[0]) == 6):
		print("Next intersection is 6, turn right to get there")
		return 1
	elif(wpm.reachedIntersection(wayPoints[0]) == 7):
		print("Next intersection is 7, go straight to get there")
		return 0
	elif(wpm.reachedIntersection(wayPoints[0]) == 8):
		print("Next intersection is 8, turn left to get there")
		return -1

def two():
	print("Intersection lane 2")
	#direction to go depends on the location of our next waypoint
	if(wpm.reachedIntersection(wayPoints[0]) == 5):
		print("Next intersection is 5, turn left to get there") 
		return -1
	elif(wpm.reachedIntersection(wayPoints[0]) == 6):
		print("Next intersection is 6, which is where we are, turn left to go in a circle")
		return -1
	elif(wpm.reachedIntersection(wayPoints[0]) == 7):
		print("Next intersection is 7, turn right to get there")
		return 1
	elif(wpm.reachedIntersection(wayPoints[0]) == 8):
		print("Next intersection is 8, go straight to get there ")
		return 0

def three():
	print("Intersection lane 3")
	#direction to go depends on the location of our next waypoint
	if(wpm.reachedIntersection(wayPoints[0]) == 5):
		print("Next intersection is 5, go straigh to get there")
		return 0
	elif(wpm.reachedIntersection(wayPoints[0]) == 6):
		print("Next intersection is 6, turn left to get there")
		return -1
	elif(wpm.reachedIntersection(wayPoints[0]) == 7):
		print("Next intersection is 7, which is where we are, turn right to go in a circle")
		return 1
	elif(wpm.reachedIntersection(wayPoints[0]) == 8):
		print("Next intersection is 8, turn right to get there")
		return 1

def four():
	print("Intersection lane 4")
	#direction to go depends on the location of our next waypoint
	if(wpm.reachedIntersection(wayPoints[0]) == 5):
		print("Next intersection is 5, turn right to get there")
		return 1
	elif(wpm.reachedIntersection(wayPoints[0]) == 6):
		print("Next intersection is 6, go straight to get there")
		return 0
	elif(wpm.reachedIntersection(wayPoints[0]) == 7):
		print("Next intersection is 7, turn left to get there")
		return -1
	elif(wpm.reachedIntersection(wayPoints[0]) == 8):
		print("Next intersection is 8, which is where we are, turn left to go in a circle")
		return -1

def five():
	global wayPoints
	print("Drove into intersection lane 5, if that is the first value of the wayPoints, removing the waypoint")
	if(wpm.reachedIntersection(wayPoints[0]) == 5):
		wayPoints = np.delete(wayPoints, 0, 0)


def six():
	global wayPoints
	print("Drove into intersection lane 6, if that is the first value of the wayPoints, removing the waypoint")
	if(wpm.reachedIntersection(wayPoints[0]) == 6):
		wayPoints = np.delete(wayPoints, 0, 0)

def seven():
	global wayPoints
	print("Drove into intersection lane 7, if that is the first value of the wayPoints, removing the waypoint")
	if(wpm.reachedIntersection(wayPoints[0]) == 7):
		wayPoints = np.delete(wayPoints, 0, 0)

def eight():
	global wayPoints
	print("Drove into intersection lane 8, if that is the first value of the wayPoints, removing the waypoint")
	if(wpm.reachedIntersection(wayPoints[0]) == 8):
		wayPoints = np.delete(wayPoints, 0, 0)

def nine():
	print("Intersection lane 9, will always be turning left")
	return -1
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn

def ten():
	print("Intersection lane 10, will always be turning right")
	return 1
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn

def eleven():
	print("Intersection lane 11, will always turn right")
	return 1
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn

def twelve():
	print("Intersection lane 12, will always turn left")
	return -1
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn

def error():
	print("Not in an intersection. Got a -1 as input")

def noIntersection():
	print("no intersection")


def useLaneNumber(num):
	switcher = {
		-1: error,
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
