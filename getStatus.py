import sys
import subprocess

while(True):

	out1=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly1}"])
	position1=out1.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x1=position1.split("x:")[1].split("\n")[0]
	y1=position1.split("y:")[1].split("\n")[0]
	z1=position1.split("z:")[1].split("\n")[0]
	x1=int(float(x1))
	y1=int(float(y1))
	z1=int(float(z1))
	print(position1)
	print("x",x1)
	print("y",y1)
	print("z",z1)
	out2=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly2}"])
	position2=out2.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x2=position2.split("x:")[1].split("\n")[0]
	y2=position2.split("y:")[1].split("\n")[0]
	z2=position2.split("z:")[1].split("\n")[0]
	x2=int(float(x2))
	y2=int(float(y2))
	z2=int(float(z2))
	print(position2)
	print("x",x2)
	print("y",y2)
	print("z",z2)
	out3=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly3}"])
	position3=out3.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x3=position3.split("x:")[1].split("\n")[0]
	y3=position3.split("y:")[1].split("\n")[0]
	z3=position3.split("z:")[1].split("\n")[0]
	x3=int(float(x3))
	y3=int(float(y3))
	z3=int(float(z3))
	print(position3)
	print("x",x3)
	print("y",y3)
	print("z",z3)
