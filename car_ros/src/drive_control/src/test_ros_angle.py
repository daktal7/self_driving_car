#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def publishAngle():
	pub = rospy.Publisher('steerAngle', Float32, queue_size=10)
	rospy.init_node('angleTalker', anonymous=False)
	rate = rospy.Rate(1)
	angle = -25
	while not rospy.is_shutdown():
		pub.publish(angle)
		if angle >= 25:
			angle = -25
		else:
			angle = angle + 10
		rate.sleep()


if __name__ == '__main__':
	try:
		publishAngle()
	except rospy.ROSInterruptException:
		pass
