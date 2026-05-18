#!/usr/bin/env python

import rospy
import actionlib
import time

from std_msgs.msg import Empty
from actions_quiz.msg import DroneCommand404Action, DroneCommand404Feedback, DroneCommand404Result


class DroneCommandServer404(object):

    # Feedback and result messages
    _feedback = DroneCommand404Feedback()
    _result   = DroneCommand404Result()

    def __init__(self):
        # Publisher pentru takeoff si land
        self._pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self._pub_land    = rospy.Publisher('/ardrone/land',    Empty, queue_size=1)

        # Creare action server
        self._as = actionlib.SimpleActionServer(
            'drone_command_server_404',      
            DroneCommand404Action,
            execute_cb=self.goal_callback_404,
            auto_start=False
        )
        self._as.start()
        rospy.loginfo('[Echipa-404] DroneCommandServer404 pornit si gata de comenzi')

    def goal_callback_404(self, goal):

        rate = rospy.Rate(1)  
        success = True

        command = goal.command.strip().upper()
        rospy.loginfo('Comanda primita', command)

        if command == 'TAKEOFF':
            # Publica comanda de decolare
            rospy.loginfo('Drona, in teorie, decoleaza')
            self._pub_takeoff.publish(Empty())

       
            start_time = rospy.Time.now()
            hover_duration = 10  

            while not rospy.is_shutdown():
         
                if self._as.is_preempt_requested():
                    rospy.loginfo('Goal TAKEOFF')
                    self._as.set_preempted()
                    success = False
                    break

                # Feedback: actiunea curenta
                self._feedback.current_action = 'TAKEOFF, drona zboara'
                self._as.publish_feedback(self._feedback)
                rospy.loginfo('Feedback: %s', self._feedback.current_action)

                elapsed = (rospy.Time.now() - start_time).to_sec()
                if elapsed >= hover_duration:
                    break

                rate.sleep()

        elif command == 'LAND':
            # Publica comanda de aterizare
            rospy.loginfo('[Echipa-404] Drona aterizeaza')
            self._pub_land.publish(Empty())

            # Trimite feedback o data pe secunda timp de ~3 secunde de aterizare
            land_duration = 3  # secunde estimate de aterizare

            start_time = rospy.Time.now()
            while not rospy.is_shutdown():
                if self._as.is_preempt_requested():
                    rospy.loginfo('[Echipa-404] Goal LAND preemptat!')
                    self._as.set_preempted()
                    success = False
                    break

                self._feedback.current_action = 'LAND - Drona aterizeaza'
                self._as.publish_feedback(self._feedback)
                rospy.loginfo('[Echipa-404] Feedback: %s', self._feedback.current_action)

                elapsed = (rospy.Time.now() - start_time).to_sec()
                if elapsed >= land_duration:
                    break

                rate.sleep()

        else:
            rospy.logwarn('Comanda necunoscuta: %s. Folositi TAKEOFF sau LAND.', command)
            success = False

        if success:
            self._as.set_succeeded(self._result)
            rospy.loginfo('Actiunea "%s" finalizata cu succes', command)


if __name__ == '__main__':
    rospy.init_node('drone_command_node_404')
    DroneCommandServer404()
    rospy.spin()
