while(True):

	out=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly1}"])
	position=out.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x=position.split("x:")[1].split("\n")[0]
	y=position.split("y:")[1].split("\n")[0]
	z=position.split("z:")[1].split("\n")[0]
	print(position)
	print("x",x)
	print("y",y)
	print("z",z)
	out2=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly2}"])
	position2=out2.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x2=position2.split("x:")[1].split("\n")[0]
	y2=position2.split("y:")[1].split("\n")[0]
	z2=position2.split("z:")[1].split("\n")[0]
	print(position2)
	print("x",x2)
	print("y",y2)
	print("z",z2)
	out3=subprocess.check_output(["rosservice", "call", "gazebo/get_model_state", "{model_name: firefly3}"])
	position3=out3.split("twist")[0].split("pose:")[1].split("orientation:")[0]
	x3=position3.split("x:")[1].split("\n")[0]
	y3=position3.split("y:")[1].split("\n")[0]
	z3=position3.split("z:")[1].split("\n")[0]
	print(position3)
	print("x",x3)
	print("y",y3)
	print("z",z3)