#!/usr/bin/env python
import rospy
from services_quiz.srv import quiz_service, quiz_serviceRequest

rospy.init_node('service_quiz_client')

rospy.loginfo("Asteptam service-ul /move_jackal_in_circle...")
rospy.wait_for_service('/move_jackal_in_circle')
rospy.loginfo("Service gasit!")

circle_service = rospy.ServiceProxy('/move_jackal_in_circle', quiz_service)

req              = quiz_serviceRequest()
req.radius       = 1.5   # metri
req.repetitions  = 3     # numarul de cercuri

result = circle_service(req)

if result.success:
    rospy.loginfo("Jackal a terminat miscarea in cerc!")
