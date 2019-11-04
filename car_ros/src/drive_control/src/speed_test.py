#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def publishSpeed():
	pub = rospy.Publisher('driveSpeed', Float32, queue_size=10)
	rospy.init_node('speedTalker', anonymous=False)
	rate = rospy.Rate(.2)
	speed = 0.04
	while not rospy.is_shutdown():
		#print("publishing speed")
		rospy.loginfo(speed)
		pub.publish(speed)
		#if speed >= 0.25:
		#	speed = 0.05
		#else:
		#	speed = speed + 0.05
		rate.sleep()


if __name__ == '__main__':
	try:
		publishSpeed()
	except rospy.ROSInterruptException:
		pass
