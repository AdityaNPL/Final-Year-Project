import os
import time

for i in range(1,6):
    os.system("rosrun rotors_gazebo waypoint_publisher 0 0 3 1 __ns:=firefly1")
    os.system("rosrun rotors_gazebo waypoint_publisher 0 "+str(i)+" 3 1 __ns:=firefly1")

