import sys
import subprocess

def roboStat(num):

	out1=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly"+str(num)+"}"])
	position1=out1.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x1=position1.split("x:")[1].split("\n")[0]
	y1=position1.split("y:")[1].split("\n")[0]
	z1=position1.split("z:")[1].split("\n")[0]
	x1=int(round(float(x1)))
	y1=int(round(float(y1)))
	z1=int(round(float(z1)))
	return [x1,y1,z1]