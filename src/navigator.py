#!/usr/bin/env python3

import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool, SetBoolResponse

class JackalNavigator:
    def __init__(self):
        rospy.init_node('jackal_navigator')

        self.active    = False
        self.scan_data = None

        # Parametri
        self.FRONT_THRESHOLD     = 0.5   # distanta la care se opreste
        self.TARGET_WALL_DIST    = 1.0   # distanta dorita fata de perete
        self.CENTER_THRESHOLD    = 0.3   # diferenta stanga/dreapta considerata "similara"
        self.LINEAR_SPEED        = 0.4   # m/s inainte
        self.ANGULAR_SPEED       = 0.5   # rad/s rotire

        # Publisher viteza
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Subscriber LIDAR
        rospy.Subscriber('/front/scan', LaserScan, self.scan_callback)

        # Service
        rospy.Service('navigate', SetBool, self.handle_service)

        rospy.loginfo("Navigator gata! Porneste cu: rosservice call /navigate true")

    def scan_callback(self, data):
        self.scan_data = data

    def get_sector_min(self, data, target_angle, width=0.25):
        """Returneaza distanta minima dintr-un sector de unghi (radiani)"""
        distances = []
        for i, r in enumerate(data.ranges):
            angle = data.angle_min + i * data.angle_increment
            if target_angle - width < angle < target_angle + width:
                if not math.isinf(r) and not math.isnan(r) and r > data.range_min:
                    distances.append(r)
        return min(distances) if distances else float('inf')

    def handle_service(self, req):
        self.active = req.data
        if self.active:
            rospy.loginfo("Navigatie PORNITA")
            return SetBoolResponse(True, "Navigatie pornita!")
        else:
            self.stop_robot()
            rospy.loginfo("Navigatie OPRITA")
            return SetBoolResponse(True, "Navigatie oprita!")

    def stop_robot(self):
        self.cmd_pub.publish(Twist())

    def navigate(self):
        if self.scan_data is None:
            rospy.logwarn("Nu exista date LIDAR inca...")
            return

        data = self.scan_data

        # Citeste distantele pe 3 sectoare
        front = self.get_sector_min(data,  0.0)
        left  = self.get_sector_min(data,  math.pi / 2)
        right = self.get_sector_min(data, -math.pi / 2)

        rospy.loginfo(f"Fata: {front:.2f}m | Stanga: {left:.2f}m | Dreapta: {right:.2f}m")

        twist = Twist()
        diff  = left - right  # pozitiv = stanga mai departe, negativ = dreapta mai departe

        if front > self.FRONT_THRESHOLD:
            # ---- MERGI INAINTE ----
            twist.linear.x = self.LINEAR_SPEED

            if abs(diff) < self.CENTER_THRESHOLD:
                # Stanga si dreapta similare -> centreaza-te
                rospy.loginfo("Centrat intre pereti")
                twist.angular.z = 0.0

            else:
                # Diferenta mare -> mentine 2m de peretele cel mai apropiat
                if left < right:
                    # Peretele din stanga e mai aproape -> vireaza usor dreapta
                    error = self.TARGET_WALL_DIST - left
                    twist.angular.z = -0.4 * error
                    rospy.loginfo(f"Prea aproape de peretele STANG (err={error:.2f}) -> virez dreapta")
                else:
                    # Peretele din dreapta e mai aproape -> vireaza usor stanga
                    error = self.TARGET_WALL_DIST - right
                    twist.angular.z = 0.4 * error
                    rospy.loginfo(f"Prea aproape de peretele DREPT (err={error:.2f}) -> virez stanga")

        else:
            # ---- OBSTACOL IN FATA ----
            twist.linear.x = 0.0

            if left >= right:
                rospy.loginfo("Obstacol in fata! Rotire STANGA (mai mult spatiu)")
                twist.angular.z = self.ANGULAR_SPEED
            else:
                rospy.loginfo("Obstacol in fata! Rotire DREAPTA (mai mult spatiu)")
                twist.angular.z = -self.ANGULAR_SPEED

        self.cmd_pub.publish(twist)

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            if self.active:
                self.navigate()
            rate.sleep()

if __name__ == '__main__':
    nav = JackalNavigator()
    nav.run()
