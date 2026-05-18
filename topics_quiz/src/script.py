#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

rospy.init_node('simple_bot')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.sleep(1.0)

def trimite(v_lin, v_ang, timp):
	msg = Twist()
	msg.linear.x, msg.angular.z = v_lin, v_ang
	pub.publish(msg)
global distanta_fata
global distanta_stanga
global distanta_dreapta

distanta_fata = data.ranges[0]
distanta_stanga = data.ranges[90]
distanta_dreapta = data.ranges[270]


rospy.init_node('stop_debug')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.Subscriber('/scan', LaserScan, cb)

rate = rospy.Rate(20)

while not rospy.is_shutdown():
    if  distanta_fata >= 1 && distanta_stanga >= 1 && distanta_dreapta>= 1 :
        trimite(0.3, 0.0)  
      elif distanta_fata < 1 && distanta_stanga >= 1 && distanta_dreapta>= 1:
        trimite(0.0, 1.0)
    if distanta_stanga	<1 :
    	trimite(0.0, -1.0)
    if distanta_dreapta <1 :
    	trimite(0.0,1.0)



