import os
import time

for i in range(2):
    os.system("rosrun rotors_gazebo waypoint_publisher 0 0 3 1 __ns:=firefly3")
    os.system("rosrun rotors_gazebo waypoint_publisher 5 0 3 1 __ns:=firefly3")
    os.system("rosrun rotors_gazebo waypoint_publisher 5 5 3 1 __ns:=firefly3")
    os.system("rosrun rotors_gazebo waypoint_publisher 0 5 3 1 __ns:=firefly3")
