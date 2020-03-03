import os
import time

for i in range(1,6):
    os.system("rosrun rotors_gazebo waypoint_publisher 2 0 3 1 __ns:=firefly3")
    os.system("rosrun rotors_gazebo waypoint_publisher 2 "+str(i)+" 3 1 __ns:=firefly3")

