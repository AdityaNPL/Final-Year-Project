import sys
import subprocess
import getStatus as gs
import random

class Ally:
    def __init__(self, id, maxIterations):
         self.id = id
         self.step = 0
         self.maxIterations = maxIterations
         self.prey = [0,0,0]
         self.r1 = [0,0,0]
         self.r2 = [0,0,0]
         self.A = [0,0,0]
         self.C = [0,0,0]
         self.D = [0,0,0]
         self.a = [2,2,2]
         self.pos = [0,0,0]
         self.history = []
         self.allies = []

    def setAllies(self, allies):
        self.allies = allies

    def calcStatus(self):
        self.pos = gs.roboStat(self.id)
        self.history.append((self.step,self.pos))
        print("pos " + str(self.id))
        print(self.pos)

    def printHistory(self):
        self.calcStatus()
        print("########################################")
        print("Robo:" + str(self.id))
        print(self.history)
        print("########################################")

    def move(self, x, y, z):
        if z<2:
            z = 2
        subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(x), str(y), str(z), str(1), "__ns:=firefly"+str(self.id)])

    def setup(self):
        self.pos = [random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
        self.move(self.pos[0], self.pos[1], self.pos[2])

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
        self.step += 1
        self.prey = prey
        self.a = 2 - 2*(self.step/self.maxIterations)
        self.randRs()
        self.calA()
        self.calC()
        self.calcStatus()
        self.calD()
        newPos = self.sub(self.prey, self.mult(self.A, self.D))
        newPos = self.checkCollision(newPos)
        self.move(newPos[0], newPos[1], newPos[2])

    def checkCollision(self,newPos):
        for ally in self.allies:
            if ally.id != self.id:
                ally.calcStatus()
                allyPos = ally.pos
                for i in range(3):
                    if allypos[i] == newPos[i]:
                        newPos[i] += 1
        return newPos
        
    def sub(self, a, b):
        return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

    def mult(self, a, b):
        return [a[0] * b[0], a[1] * b[1], a[2] * b[2]]
