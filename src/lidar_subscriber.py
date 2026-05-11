#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

def callback(data):
    rospy.loginfo("=== Date LIDAR ===")
    rospy.loginfo(f"Numar puncte: {len(data.ranges)}")
    rospy.loginfo(f"Distanta minima: {data.range_min:.2f} m")
    rospy.loginfo(f"Distanta maxima: {data.range_max:.2f} m")
    
    valid = [r for r in data.ranges if data.range_min < r < data.range_max]
    if valid:
        rospy.loginfo(f"Cel mai apropiat obiect: {min(valid):.2f} m")

def listener():
    print("Scriptul a pornit!")
    rospy.init_node('lidar_subscriber', anonymous=True)
    rospy.Subscriber('/front/scan', LaserScan, callback)
    rospy.loginfo("Ascult datele LIDAR...")
    rospy.spin()

if __name__ == '__main__':
    listener()
