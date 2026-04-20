#! /usr/bin/env python

import rospy                              			# Import the Python library for ROS
from std_msgs.msg import Int32             		# Import the Int32 message from the std_msgs package
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

rospy.init_node('topic_publisher')         		# Initiate a Node named 'topic_publisher'

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.sleep(1.0)
 
def trimite(v_lin, v_ang):
    """
    Publică viteza liniară și unghiulară pe topicul /cmd_vel
    """
    msg = Twist()
    msg.linear.x = v_lin
    msg.angular.z = v_ang
    pub.publish(msg)

def cb(data):
    """
    Funcția de callback pentru /scan. 
    Aici se actualizează distanțele folosind datele live din senzor.
    """
    global distanta_fata, distanta_stanga, distanta_dreapta
    
    # Ne asigurăm că senzorul are cel puțin 271 de raze înainte să citim 
    # pentru a evita eroarea "index out of range"
    if len(data.ranges) > 270:
        distanta_fata = data.ranges[0]
        distanta_stanga = data.ranges[90]
        distanta_dreapta = data.ranges[270]

# 1. Inițializăm nodul (o singură dată)
rospy.init_node('robot_evitare_obstacole')

# 2. Definim Publisher-ul
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# 3. Definim Subscriber-ul care apelează funcția 'cb'
rospy.Subscriber('/scan', LaserScan, cb)

# Așteptăm puțin pentru ca publisher-ul/subscriber-ul să se conecteze la ROS Master
rospy.sleep(1.0)

# Rata de rulare a buclei (20 Hz)
rate = rospy.Rate(20)

while not rospy.is_shutdown():
    # Am înlocuit && cu and și am corectat indentările
    if distanta_fata >= 1 and distanta_stanga >= 1 and distanta_dreapta >= 1:
        trimite(0.3, 0.0)   # Mergi înainte
        
    elif distanta_fata < 1 and distanta_stanga >= 1 and distanta_dreapta >= 1:
        trimite(0.0, 1.0)   # Rotește stânga dacă e obstacol în față
        
    elif distanta_stanga < 1:
        trimite(0.0, -1.0)  # Rotește dreapta dacă e obstacol în stânga
        
    elif distanta_dreapta < 1:
        trimite(0.0, 1.0)   # Rotește stânga dacă e obstacol în dreapta
        
    # Obligatoriu pentru a respecta rata de 20Hz și a nu bloca procesorul
    rate.sleep()
