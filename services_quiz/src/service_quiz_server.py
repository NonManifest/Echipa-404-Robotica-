#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from services_quiz.srv import services_quiz, services_quizResponse

cmd_pub = None

def move_in_circle_callback(request):
    twist = Twist()

    linear_speed = 2

    angular_speed = linear_speed / request.radius

    twist.linear.x  = linear_speed
    twist.angular.z = angular_speed

    rate = rospy.Rate(10) 
    end_time = rospy.Time.now() + rospy.Duration(request.duration)

    while rospy.Time.now() < end_time and not rospy.is_shutdown():
        cmd_pub.publish(twist)
        rate.sleep()

    cmd_pub.publish(Twist())
    rospy.loginfo("Cerc gata")

    return services_quizResponse(success=True)


if __name__ == '__main__':
    rospy.init_node('services_quiz_server')

    cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.sleep(1.0)

    service = rospy.Service('/move_jackal_in_circle',
                            JackalCircle,
                            move_in_circle_callback)

    rospy.loginfo("Service activ")
    rospy.spin()
