"""
This file contains the code to retrive live data from the simulator during a simulation
"""

import sys
import subprocess

def roboStat(num):

	out=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly"+str(num)+"}"])
	position=out.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x=position.split("x:")[1].split("\n")[0]
	y=position.split("y:")[1].split("\n")[0]
	z=position.split("z:")[1].split("\n")[0]
	x=int(round(float(x)))
	y=int(round(float(y)))
	z=int(round(float(z)))
	return [x,y,z]
