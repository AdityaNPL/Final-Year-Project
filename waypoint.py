import os
import sys

for i in range(1,21):
    os.system("rosrun rotors_gazebo waypoint_publisher 0 0 1 20 __ns:=firefly1")
    os.system("rosrun rotors_gazebo waypoint_publisher 0 1 1 20 __ns:=firefly2")
    os.system("rosrun rotors_gazebo waypoint_publisher 0 2 1 20 __ns:=firefly3")
    time.sleep(2)
    os.system("rosrun rotors_gazebo waypoint_publisher "+str(i)+" 0 1 20 __ns:=firefly1")
    os.system("rosrun rotors_gazebo waypoint_publisher "+str(i)+" 1 1 20 __ns:=firefly2")
    os.system("rosrun rotors_gazebo waypoint_publisher "+str(i)+" 2 1 20 __ns:=firefly3")
    time.sleep(2)
