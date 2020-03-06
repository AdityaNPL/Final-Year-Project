import os
import time

for i in range(2):
    os.system("rosrun rotors_gazebo waypoint_publisher 0 0 1 1 __ns:=firefly1")
    os.system("rosrun rotors_gazebo waypoint_publisher 1 0 1 1 __ns:=firefly1")
    os.system("rosrun rotors_gazebo waypoint_publisher 1 1 1 1 __ns:=firefly1")
    os.system("rosrun rotors_gazebo waypoint_publisher 0 1 1 1 __ns:=firefly1")
