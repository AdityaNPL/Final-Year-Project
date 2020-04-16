from GWO import Ally
from GWO import Adversary

class EAsim:
	def __init__(self):
		self.robotNum = 5
		self.robots = []
		self.allies = []
		self.maxIterations = 100
		self.realSim = False

		for i in range(self.robotNum-1):
			self.robots.append(Ally.Ally(i+1,self.maxIterations, self.realSim))
			self.allies.append(self.robots[i]) 

		self.robots.append(Adversary.Adversary(self.robotNum, self.maxIterations, self.realSim))

		for i in range(self.robotNum):
			self.robots[i].setup()
			self.robots[i].setAllies(self.allies)

		for i in range(self.robotNum - 1):
			self.robots[i].setAdv(self.robots[self.robotNum-1])

	def run(self):
		for i in range(self.maxIterations):
			print(str(i+1) + " / " + str(self.maxIterations))
			for i in range(self.robotNum):
				self.robots[i].calcWaypoints()
			for i in range(self.robotNum):
				self.robots[i].runMove()

	def printToFile(self):
		for i in range(self.robotNum):
			self.robots[i].printHistory()
