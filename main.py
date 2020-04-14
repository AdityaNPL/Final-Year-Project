import Ally

allies = []
maxIterations = 5
robots = 4
# Adv
Ally.Ally(robots+1,maxIterations).move(5,5,35)

for i in range(robots):
	allies.append(Ally.Ally(i+1,maxIterations))

for i in range(robots):
	allies[i].setup()
	allies[i].setAllies(allies)


for i in range(maxIterations):
	print(str(i+1) + " / " + str(maxIterations))
	for i in range(robots):
			allies[i].calcWaypoints()
	for i in range(robots):
			try:
				allies[i].runMove()
			except:
				print("e")

for i in range(robots):
	allies[i].printHistory()

