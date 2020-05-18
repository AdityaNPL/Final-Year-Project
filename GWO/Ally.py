"""
This file contains the class for the Ally.
This class is responsible for moving the allies during the simulation using the GWO waypoint algorithm approach.
This is based on and adapted from the implementation in the paper by Mirjalili et al.
[S. Mirjalili, S.M. Mirjalili, and A. Lewis. “Grey Wolf Optimizer”.
In: Advances in Engineering Software. Vol. 69. 2014, pp. 46–61.
doi: https://doi.org/10.1016/j.advengsoft.2013.12.007.
url: http://www.sciencedirect.com/science/article/pii/S0965997813001853.]
"""

import sys
import subprocess
import getStatus as gs
import random
import csv
import numpy as np
import math

class Ally:
    def __init__(self, id, maxIterations, maxSpeed, decreasingVal, realSim):
         self.id = id
         self.step = 0
         self.maxIterations = maxIterations
         self.maxSpeed = maxSpeed
         self.decreasingVal = decreasingVal
         self.prey = [0,0,0]
         self.r1 = [0,0,0]
         self.r2 = [0,0,0]
         self.A = [0,0,0]
         self.C = [0,0,0]
         self.D = [0,0,0]
         self.a = [2,2,2]
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

    def randRs(self):
        self.r1 = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
        self.r2 = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]

    def calA(self):
        self.A = self.sub(self.mult([2*self.a,2*self.a,2*self.a], self.r1), [self.a,self.a,self.a])

    def calC(self):
        self.C = [2*self.r2[0],2*self.r2[1],2*self.r2[2]]

    def calD(self):
        self.D = self.sub(self.mult(self.C, self.prey), self.pos)
        for i in range(3):
            if self.D[i] < 0:
                self.D[i] *= -1


    def encircle(self, prey):
        self.prey = prey
        self.a = self.decreasingVal - self.decreasingVal*(self.step/self.maxIterations)
        self.randRs()
        self.calA()
        self.calC()
        self.calcStatus()
        self.calD()
        newPos = self.sub(self.prey, self.mult(self.A, self.D))
        return newPos

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

    def sub(self, a, b):
        return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

    def mult(self, a, b):
        return [a[0] * b[0], a[1] * b[1], a[2] * b[2]]

    def getErroredPostion(self, pos):
        distanceToOject = self.calcDistanceBetweenPoints(self.pos, pos)
        errorValue = (np.random.normal(distanceToOject, distanceToOject/10, 1)[0]) - distanceToOject
        return [pos[0] + errorValue, pos[1] + errorValue, pos[2] + errorValue]

    def calcDistanceBetweenPoints(self, selfPoint, refPoint):
        ans = 0
        for i in range(len(selfPoint)):
            ans += (selfPoint[i]-refPoint[i])**2
        return math.sqrt(ans)

    def calcWaypoints(self):
        self.calcStatus()
        self.step += 1
        self.newPos = self.encircle(self.getErroredPostion(self.adv.pos))
        for i in range(3):
            diff = self.newPos[i] - self.pos[i]
            if abs(diff) > self.maxSpeed:
                self.newPos[i] = self.pos[i] + ((diff/diff) * self.maxSpeed)
        self.checkCollision()

    def runMove(self):
        self.move(self.newPos[0], self.newPos[1], self.newPos[2])
