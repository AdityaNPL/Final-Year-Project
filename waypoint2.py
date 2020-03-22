import sys
import subprocess
import getStatus as gs

num = 2 
values = []
for i in range(2):
    subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(0), str(0), str(num), str(1), "__ns:=firefly"+str(num)])
    values.append(gs.roboStat(num))
    subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(0), str(5), str(num), str(1), "__ns:=firefly"+str(num)])
    values.append(gs.roboStat(num))
    subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(5), str(5), str(num), str(1), "__ns:=firefly"+str(num)])
    values.append(gs.roboStat(num))
    subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(5), str(0), str(num), str(1), "__ns:=firefly"+str(num)])
    values.append(gs.roboStat(num))


print("\n")
print(values)