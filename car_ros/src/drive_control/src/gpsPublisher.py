#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32, Int32
from drive_control.msg import gps
import intersectionLaneSwitches as ils
import wpManager as wpm
import requests
import time
import numpy as np
import testIntersections as ti
#

#This publisher will publish the following:
# 1: turn right
# -1: turn left
# 0: go straight
# 2: stop
# 4: raise warning intersection flag
# 5: tell traffic light detection to start running
# 6: lost GPS
# 7: got GPS back
# 40: turn right, stop sign
# -40: turn left, stop sign

#squared distance to save computation
MAX_COOR_DIST = 150**2
COOR_TIMEOUT = 20 #determines how much time we'll wait for a coordinate

def isGoodCoor(coor1,coor2):
	if coor1 is None or coor2 is None:
		return True
	dist = ((coor1[1]-coor2[1])**2)+((coor1[0]-coor2[0])**2)
	return dist < MAX_COOR_DIST

def verifyCoor(coor, prevCoor,pub):
	if not isGoodCoor(coor, prevCoor):
		print("gpspub: BAD COOR")
		# begTime = time.time()
		# time = time.time() - begTime
		pub.publish(6)  # stop the car and wait until we get the coordinate
		rate2 = rospy.Rate(7)
		while not isGoodCoor(ti.getCoor("Green"), prevCoor):  # and time < COOR_TIMEOUT:
			# time = time.time
			rate2.sleep()
		pub.publish(7)  # tell the drive that we are good again

def publishIntersection():
	pub = rospy.Publisher('intersection', Int32, queue_size=10)
	rospy.init_node('intersection_pub', anonymous=False)
	rate = rospy.Rate(5)
	prevInter = -1
	prevCoor = None
	while not rospy.is_shutdown():
		coor = ti.getCoor("Green")
		coor = (abs(coor[0]),abs(coor[1]))

		#verifyCoor(coor, prevCoor, pub) #this tests to see if we're getting a bogus coordinate, just comment out if you want to disable
		#prevCoor = coor

		inter = wpm.reachedWarningIntersection(coor)

        #check to see if we're in a warning intersection
		if inter != -1:
			if inter != prevInter:
				turn = ils.useLaneNumber(inter,prevInter) #check to see if we are going to turn or not
				if turn is not None:
					prevInter = inter
					pub.publish(4)
					print("gpsPub: In warning intersection", prevInter)
					# check if we are in the stoplight intersections
					rateInner = rospy.Rate(10)
					while wpm.reachedStopIntersection(coor) == -1:
						coor = ti.getCoor("Green")
						coor = (abs(coor[0]),abs(coor[1]))
						rateInner.sleep()
					print("publishing turn %d", turn)
					pub.publish(2)
					if inter < 5:
						pub.publish(5)
					else:
						time.sleep(1.5)
					pub.publish(turn)
			#print("found intersection. Intersection value: ", inter)
		#if speed >= 0.25:
		#	speed = 0.05
		#else:
		#	speed = speed + 0.05
		rate.sleep()


if __name__ == '__main__':
	try:
		publishIntersection()
	except rospy.ROSInterruptException:
		pass
 
#import rospy
#import wpManager as wpm
#from drive_control.msg import gps

#<node pkg="drive_control" type="gpsPublisher.py" name="gps_publisher" output="screen">
#</node>


#def publishIntersection():
	#pub = rospy.Publisher('intersectionNumber',int,queue_size=1)
	#rospy.init_node('gpsTalker', anonymous = False)
	#rate = rospy.Rate(.1)
	#intersect = wpm.reachedIntersection(gps())
	#while not rospy.is_shutdown():
	#	pub.publish(intersect)
	#	rate.sleep()

#if __name__ == '__main__':
#	try:
#		publishIntersection()
#	except rospy.ROSInterruptException:
#		pass


# class gpsPublisher:
#     def __init__(self):
#         self.gpsPub = rospy.Publisher("gps_coord",gps, queue_size = 1)

#     def talker():
# 	    myGps = gps()
# 	    myGps.x = 2
# 	    myGps.y = 3
#         self.gpsPub.publish(myGps)

# myGPS = gpsPublisher()
# rospy.init_node('gps_publisher', anonymous = False)
# rate = rospy.Rate(1)
# while not rospy.is_shutdown():
#     myGPS.talker()
#     rate.sleep()





#*********************Dakotas code******************

#!/usr/bin/env python

# import rospy
# from std_msgs.msg import Float32

# def publishSpeed():
# 	pub = rospy.Publisher('driveSpeed', Float32, queue_size=10)
# 	rospy.init_node('speedTalker', anonymous=False)
# 	rate = rospy.Rate(.1)
# 	speed = 0.01
# 	while not rospy.is_shutdown():
# 		pub.publish(speed)
# 		#if speed >= 0.25:
# 		#	speed = 0.05
# 		#else:
# 		#	speed = speed + 0.05
# 		rate.sleep()


# if __name__ == '__main__':
# 	try:
# 		publishSpeed()
# 	except rospy.ROSInterruptException:
# 		pass
