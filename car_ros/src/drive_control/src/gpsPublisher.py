#!/usr/bin/env
 
import rospy
from drive_control.msg import gps


#class gpsPublisher:
#    def __init__(self):
#        self.gpsPub = rospy.Publisher("gps_topic", )

def talker():
    pub = rospy.Publisher('/gps_coord',gps,queue_size = 1)
    rospy.init_node('gps_publisher')
    rate = rospy.Rate(1)
	myGps = gps()
	myGps.x = 2
	myGps.y = 3
    while not rospy.is_shutdown():
        pub.publish(myGps)
        rate.sleep()

talker()
