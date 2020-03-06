import os
import time

for i in range(2):
    os.system("rosrun rotors_gazebo waypoint_publisher 0 0 2 1 __ns:=firefly2")
    os.system("rosrun rotors_gazebo waypoint_publisher 5 0 2 1 __ns:=firefly2")
    os.system("rosrun rotors_gazebo waypoint_publisher 5 5 2 1 __ns:=firefly2")
    os.system("rosrun rotors_gazebo waypoint_publisher 0 5 2 1 __ns:=firefly2")
