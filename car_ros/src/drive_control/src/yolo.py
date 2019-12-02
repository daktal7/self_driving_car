#!/usr/bin/env python

# USAGE
# sudo MXNET_CUDNN_AUTOTUNE_DEFAULT=0 python3 yolo.py
# OPTIONAL PARAMETERS
# -c/--confidence (.0-1.0) (detected objects with a confidence higher than this will be used)

# import the necessary packages
#from car_control import steer, drive
import rospy
from std_msgs.msg import Char


pub = rospy.Publisher("light", Char, queue_size = 1)

rospy.init_node('yolo_node', anonymous=False)
rate = rospy.Rate(1)
oldLight = 'q'
while not rospy.is_shutdown():
    f = open("/home/nvidia/Desktop/light.txt", "r")
    light = f.read(1)
    print(light)
    if light != oldLight:
        pub.publish(light)
    f.close()
    rate.sleep()



