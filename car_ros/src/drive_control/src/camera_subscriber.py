#!/usr/bin/env python
#Python_MainV2
# Python Main

import cv2
import time
from signal import signal, SIGINT
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_displayer:
	def __init__(self):
		self.bridge = CvBridge()		
		self.image_sub = rospy.Subscriber("video_topic", Image, self.display)
	
	def display(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
		except CvBridgeError as e:
			print(e)
		cv2.imshow("Image Window", cv_image)
		cv2.waitKey(3)


id = image_displayer()
rospy.init_node('player', anonymous = True)
rospy.spin()
