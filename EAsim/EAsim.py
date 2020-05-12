from GWO import Ally
from GWO import Adversary
from Tester import RobotTester as rt
import math
class EAsim:
	def __init__(self, genes):
		self.robotNum = 4
		self.robots = []
		self.allies = []
		self.genes = genes # iterations, maxSpeed, decreasingVal
		self.maxIterations = self.genes["iterations"]
		self.maxSpeed = self.genes["maxSpeed"]
		self.decreasingVal = self.genes["decreasingVal"]
		self.realSim = False

		for i in range(self.robotNum-1):
			self.robots.append(Ally.Ally(i+1,self.maxIterations, self.maxSpeed, self.decreasingVal, self.realSim))
			self.allies.append(self.robots[i])

		self.robots.append(Adversary.Adversary(self.robotNum, self.maxIterations, self.maxSpeed, self.realSim))

		for i in range(self.robotNum):
			self.robots[i].setup()
			self.robots[i].setAllies(self.allies)

		for i in range(self.robotNum - 1):
			self.robots[i].setAdv(self.robots[self.robotNum-1])

	def run(self):
		done = False
		for i in range(self.maxIterations):
			positions = []
			# print(str(i+1) + " / " + str(self.maxIterations))
			for i in range(self.robotNum):
				self.robots[i].calcWaypoints()

			for i in range(self.robotNum):
				self.robots[i].runMove()
				positions.append(self.robots[i].pos)

			for i in range(len(positions)-1):
				if self.checkEqualPos(positions[i], positions[len(positions)-1]):
					done = True
					break
			if done:
				break

	def printToFile(self, write):
		for i in range(self.robotNum):
			self.robots[i].printHistory(write)

	def checkEqualPos(self, pos1, pos2):
		distance = 0.5
		return abs(pos1[0] - pos2[0]) <= distance and abs(pos1[1] - pos2[1]) <= distance and abs(pos1[2] - pos2[2]) <= distance

	def fitness(self):
		self.printToFile(False)

		finalTime = 0
		finalLineOfSight = 0
		finalBlastRange = 0
		finalAverageChange = 0

		robot = self.robots[self.robotNum-1]
		data = robot.dataToAnalyse
		avgDistFromCenter = min((robot.avgDistFromCenter / len(data)) / 10000, 1)
		oppPos = []
		oppSpeed = []
		for row in data:
			oppPos.append((float(row[1]), float(row[2]), float(row[3])))
			oppSpeed.append((float(row[4]), float(row[5]), float(row[6])))
		test = rt.RobotTester([oppPos,oppSpeed], [oppPos,oppSpeed])
		changesInAngles = test.changeOfAngleOfSelf()
		avgChangeInAngle_adv = abs(math.degrees(sum(changesInAngles)/len(changesInAngles)))/360.0
		finalTime = test.timeTakenToCapture()
		finalTimeFactor = 1 - finalTime /self.maxIterations
		for i in range(self.robotNum - 1):
			robot = self.robots[i]
			data = robot.dataToAnalyse
			selfPos = []
			selfSpeed = []
			for row in data:
				selfPos.append((float(row[1]), float(row[2]), float(row[3])))
				selfSpeed.append((float(row[4]), float(row[5]), float(row[6])))

			test = rt.RobotTester([selfPos,selfSpeed], [oppPos,oppSpeed])

			lineOfSight = test.countLineOfSight()
			finalLineOfSight += (lineOfSight[0]*1.0/lineOfSight[1])
			blastRange = test.countBlastRange()
			finalBlastRange += (blastRange[0]*1.0/blastRange[1])
			changesInAngles = test.changeOfAngleOfSelf()
			finalAverageChange += abs(math.degrees(sum(changesInAngles)/len(changesInAngles)))/360.0

		finalLineOfSight = finalLineOfSight / (self.robotNum - 1)
		finalBlastRange = finalBlastRange / (self.robotNum - 1)
		finalAverageChange = 1 - (finalAverageChange / (self.robotNum - 1))

		if finalTimeFactor > 0:
			print("Finished Early")
			print(finalTime, finalTimeFactor)

		fitnessVal = 5*finalTimeFactor + 19*finalLineOfSight + 19*finalBlastRange + 19*finalAverageChange + 19*avgDistFromCenter + 19*avgChangeInAngle_adv
		# print(finalTime,  finalLineOfSight, finalBlastRange, finalAverageChange, avgDistFromCenter, avgChangeInAngle_adv)
		# print(fitnessVal)
		return fitnessVal
