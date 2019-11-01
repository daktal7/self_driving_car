#!/usr/bin/env python

def one():
	print("Intersection lane 1")
	#direction to go depends on the location of our next waypoint

def two():
	print("Intersection lane 2")
	#direction to go depends on the location of our next waypoint

def three():
	print("Intersection lane 3")
	#direction to go depends on the location of our next waypoint

def four():
	print("Intersection lane 4")
	#direction to go depends on the location of our next waypoint

def five():
	print("Drove into intersection lane 5, no action")

def six():
	print("Drove into intersection lane 6, no action")

def seven():
	print("Drove into intersection lane 7, no action")

def eight():
	print("Drove into intersection lane 8, no action")

def nine():
	print("Intersection lane 9")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn

def ten():
	print("Intersection lane 10")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn

def eleven():
	print("Intersection lane 11")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a right turn

def twelve():
	print("Intersection lane 12")
	#needs to suspend the normal driving angle procedures
	#Might need to go straight still for a bit, then make a left turn

def noIntersection():
	print("no intersection")


def useLaneNumber(num):
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
