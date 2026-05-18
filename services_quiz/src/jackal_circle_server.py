#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from services_quiz.srv import JackalCircle, JackalCircleResponse

cmd_pub = None

def move_in_circle_callback(request):
    rospy.loginfo("Service apelat: duration=%d s, radius=%.2f m",
                  request.duration, request.radius)

    twist = Twist()

    linear_speed = 1

    if request.radius <= 0:
        rospy.logerr(">0")
        return JackalCircleResponse(success=False)

    angular_speed = linear_speed / request.radius

    twist.linear.x  = linear_speed
    twist.angular.z = angular_speed

    rate = rospy.Rate(10) 
    end_time = rospy.Time.now() + rospy.Duration(request.duration)

    rospy.loginfo("Jackal merge")

    while rospy.Time.now() < end_time and not rospy.is_shutdown():
        cmd_pub.publish(twist)
        rate.sleep()

    cmd_pub.publish(Twist())
    rospy.loginfo("Jackal s-a oprit. Miscare completa")

    return JackalCircleResponse(success=True)


if __name__ == '__main__':
    rospy.init_node('jackal_circle_server')

    cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.sleep(1.0)

    service = rospy.Service('/move_jackal_in_circle',
                            JackalCircle,
                            move_in_circle_callback)

    rospy.loginfo("Service /move_jackal_in_circle este ACTIV.")
    rospy.spin()
