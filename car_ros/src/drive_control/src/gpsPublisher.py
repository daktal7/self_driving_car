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
def publishIntersection():
	pub = rospy.Publisher('intersection', Int32, queue_size=1)
	rospy.init_node('intersection_pub', anonymous=False)
	rate = rospy.Rate(1)
	prevInter = -1
	while not rospy.is_shutdown():
		# grab the gps point
		
        # check to see if we're in the intersection
		coor = ti.getCoor("Green")
		if coor[0] < 0:
			coor = (-1*coor[0],-1*coor[1])
		inter = wpm.reachedIntersection(coor) #change this to the right color
        # if we are in an intersection, publish where we should turn
        # -1 is left 0 is straight, 1 is right
		if inter != -1:
			if inter != prevInter:
				prevInter = inter
				rospy.loginfo(inter)
				turn = ils.useLaneNumber(inter)
				if turn is not None:
					print("publishing turn %d", turn)
					pub.publish(2)
					time.sleep(1.5)
					pub.publish(turn)
					time.sleep(2.5)
					pub.publish(3)
				else:
					print("not publishing turn")
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
