#!/usr/bin/env python
#Python_MainV2
# Python Main

import cv2
import time
from signal import signal, SIGINT
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
#from std_msgs.msg import Float32

class image_converter:
	def __init__(self):
		print("image converter")
		self.image_pub = rospy.Publisher("video_topic", Image, queue_size=1)
		self.bridge = CvBridge()
	
	def publish_frame(self, frame):
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)))
		except CvBridgeError as e:
			print(e)

# Function to correctly exit program
def handler(signal_received, frame):
    command = "!speed0\n"
    ser.write(command.encode())
    cap.release()
    print('CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)
print('Running. Press CTRL-C to exit')
cap = cv2.VideoCapture("/dev/video2",cv2.CAP_V4L)
#while not cap.isOpened():
#	print("trying again")
#	cap = cv2.VideoCapture("/dev/video2",cv2.CAP_V4L)
ic = image_converter()
rospy.init_node('video', anonymous = False)
while(cap.isOpened()):
	try:
		_, frame = cap.read()
		ic.publish_frame(frame)
	except KeyboardInterrupt:
		print("Shutting Down Video")
		break
cv2.destroyAllWindows()

