cmake_minimum_required(VERSION 3.0.2)
project(actions_quiz)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  actionlib
  actionlib_msgs
)

# Adauga fisierul .action custom al Echipei 404
add_action_files(
  FILES
  DroneCommand404.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
  rospy
  std_msgs
  actionlib
  actionlib_msgs
)
