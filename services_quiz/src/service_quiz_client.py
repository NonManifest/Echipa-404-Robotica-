#!/usr/bin/env python

import rospy
from services_quiz.srv import services_quiz, services_quizRequest

rospy.init_node('service_quiz_client')

rospy.loginfo("Asteptam service-ul /move_jackal_in_circle...")
rospy.wait_for_service('/move_jackal_in_circle')
rospy.loginfo("Service gasit!")

circle_service = rospy.ServiceProxy('/move_jackal_in_circle', JackalCircle)

req = services_quizRequest()
req.radius   = 1.5    # metri
req.duration = int((2*3.14*req.radius/2)+(2*3.14*req.radius%2))     # secunde

result = circle_service(req)

if result.success:
    rospy.loginfo("Jackal a terminat miscarea in cerc!")

