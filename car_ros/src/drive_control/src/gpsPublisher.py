#!/usr/bin/env
 
import rospy
import wpManager as wpm
from drive_control.msg import gps


class gpsPublisher:
    def __init__(self):
        self.gpsPub = rospy.Publisher("gps_coord",gps, queue_size = 1)

    def talker():
	    myGps = gps()
	    myGps.x = 2
	    myGps.y = 3
        self.gpsPub.publish(myGps)

myGPS = gpsPublisher()
rospy.init_node('gps_publisher', anonymous = False)
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    myGPS.talker()
    rate.sleep()

