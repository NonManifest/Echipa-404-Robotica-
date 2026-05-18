#!/usr/bin/env python

import rospy
from jackal_pkg.srv import JackalCircle, JackalCircleRequest

rospy.init_node('jackal_circle_client')

rospy.loginfo("Asteptam service-ul /move_jackal_in_circle...")
rospy.wait_for_service('/move_jackal_in_circle')
rospy.loginfo("Service gasit")

circle_service = rospy.ServiceProxy('/move_jackal_in_circle', JackalCircle)

req = JackalCircleRequest()
req.duration = 40      # secunde
req.radius   = 1.5    # metri

result = circle_service(req)

if result.success:
    rospy.loginfo("Jackal a terminat miscarea")
else:
    rospy.logerr("Nu vrea")
