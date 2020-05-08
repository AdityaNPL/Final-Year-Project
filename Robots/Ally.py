import sys
import subprocess
import getStatus as gs
import random
import csv

class Ally:
    def __init__(self, id, realSim):
         self.id = id
         self.step = 0
         self.maxSpeed = 5
         self.prey = [0,0,0]
         self.pos = [0,0,0]
         self.history = {}
         self.allies = []
         self.adv = None
         self.newPos = [0,0,0]
         self.realSim = realSim
         self.dataToAnalyse = []

    def setAllies(self, allies):
        self.allies = allies

    def setAdv(self, adv):
        self.adv = adv

    def calcStatus(self):
        if self.realSim:
            self.pos = gs.roboStat(self.id)
        self.history[self.step] = self.pos

    def printHistory(self, write):
        self.calcStatus()
        # print("########################################")
        # print("Robo:" + str(self.id))

        posList = []
        for key in self.history.keys():
            posList.append([key,self.history[key][0],self.history[key][1],self.history[key][2]])
        for i in range(len(posList)):
            speed = [0,0,0]
            pos = posList[i]
            if i != 0:
                speed = [pos[1] - posList[i-1][1], pos[2]- posList[i-1][2], pos[3]- posList[i-1][3]]
            self.dataToAnalyse.append((pos[0],pos[1],pos[2],pos[3],speed[0],speed[1],speed[2]))

        if write:
            with open('./DataDump/data_'+str(self.id)+'.csv', 'w+') as out:
                for data in self.dataToAnalyse:
                    out.write("%s,%s,%s,%s,%s,%s,%s\n"%data)

    def move(self, x, y, z):
        if z<2:
            z = 2
        if self.realSim:
            subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(x), str(y), str(z), str(0), "__ns:=firefly"+str(self.id)])
        else:
            self.pos = [x,y,z]

    def setup(self):
        x,y,z = (random.uniform(-50,50),random.uniform(-50,50),0)
        if self.realSim:
            subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(x), str(y), str(z), str(0), "__ns:=firefly"+str(self.id)])
        # print(x,y,z)

    def checkCollision(self):
        if self.newPos[2]<10:
            self.newPos[2] = 10
        for ally in self.allies:
            if ally.id != self.id:
                ally.calcStatus()
                allyPos = ally.pos
                for i in range(3):
                    if allyPos[i] == self.newPos[i]:
                        self.newPos[i] += 1

    def calcWaypoints(self, direction):
        self.calcStatus()
        for i in range(3):
            self.newPos[i] = self.pos[i] + (direction[i] * self.maxSpeed)
        self.checkCollision()

    def runMove(self):
        self.move(self.newPos[0], self.newPos[1], self.newPos[2])
