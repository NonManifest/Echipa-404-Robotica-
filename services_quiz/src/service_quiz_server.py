#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from services_quiz.srv import quiz_service, quiz_serviceResponse
import math

cmd_pub = None

def move_in_circle_callback(request):
    twist = Twist()
    linear_speed  = 1.0
    angular_speed = linear_speed / request.radius   # omega = v / r

    twist.linear.x  = linear_speed
    twist.angular.z = angular_speed

    # timp pentru un cerc complet = circumferinta / viteza
    time_per_circle = (2 * math.pi * request.radius) / math.sqrt(linear_speed*linear_speed+angular_speed*angular_speed)
    total_duration  = time_per_circle * request.repetitions

    rospy.loginfo("Raza: %.2f m | Repetitii: %d | Durata totala: %.2f s",
                  request.radius, request.repetitions, total_duration)

    rate     = rospy.Rate(10)
    end_time = rospy.Time.now() + rospy.Duration(total_duration)

    while rospy.Time.now() < end_time and not rospy.is_shutdown():
        cmd_pub.publish(twist)
        rate.sleep()

    cmd_pub.publish(Twist())   # oprire
    rospy.loginfo("Cerc(uri) gata!")
    return quiz_serviceResponse(success=True)

if __name__ == '__main__':
    rospy.init_node('service_quiz_server')
    cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.sleep(1.0)
    service = rospy.Service('/move_jackal_in_circle',
                            quiz_service,
                            move_in_circle_callback)
    rospy.loginfo("Service activ: /move_jackal_in_circle")
    rospy.spin()
