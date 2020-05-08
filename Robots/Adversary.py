import math
import time
import sys
import subprocess
import getStatus as gs
import random
import csv

class Adversary():

    def __init__(self, id, realSim):
        self.id = id
        self.step = 0
        self.maxSpeed = 5
        self.pos = [0,0,0]
        self.history = {}
        self.allies = []
        self.newPos = [0,0,0]
        self.realSim = realSim
        self.timer_start = time.time()
        self.timer_end = time.time()
        self.no_of_move_calls = 0
        # self.grid_distribution = [[0 for i in range(self.grid_ui_obj.grid_width/100+1)] for j in range(self.grid_ui_obj.grid_height/100+1)]
        self.avgDistFromCenter = 0
        self.dataToAnalyse = []

    def setAllies(self, allies):
        self.allies = allies

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
            with open('./DataDump/data_adv'+str(self.id)+'.csv', 'w+') as out:
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
        self.pos = [random.uniform(-10,10),random.uniform(-10,10),random.uniform(40,60)]
        self.move(self.pos[0], self.pos[1], self.pos[2])

    def calcVector(self):
        direction = [0,0,0]
        for opponent in self.allies:
            vector = list(map(lambda x: x*0.1, self.getVector(opponent.pos, self.pos)))
            for i in range(3):
                direction[i] += vector[i]

        vectorToCenter = self.getVector(self.pos, [0,0,50])
        vectors = [vectorToCenter]
        self.avgDistFromCenter += self.magnitude(vectorToCenter)
        vectors.append(self.getVector([self.pos[0],self.pos[1],200], self.pos))
        vectors.append(self.getVector([self.pos[0],self.pos[1],2], self.pos))
        vectors.append(self.getVector([self.pos[0],-200,self.pos[2]], self.pos))
        vectors.append(self.getVector([self.pos[0],200,self.pos[2]], self.pos))
        vectors.append(self.getVector([-200,self.pos[1],self.pos[2]], self.pos))
        vectors.append(self.getVector([200,self.pos[1],self.pos[2]], self.pos))
        for vector in vectors:
            for i in range(3):
                direction[i] += vector[i]

        for i in range(3):
            if abs(direction[i]) > self.maxSpeed:
                direction[i] = direction[i]/direction[i] * self.maxSpeed

        return [self.pos[0] + direction[0], self.pos[1] + direction[1], self.pos[2] + direction[2]]

    def getVector(self, start, end):
        return[end[0]-start[0], end[1]-start[1], end[2]-start[2]]

    def calcWaypoints(self):
        self.calcStatus()
        self.step += 1
        self.newPos = self.calcVector()


    def runMove(self):
        self.move(self.newPos[0], self.newPos[1], self.newPos[2])

    def magnitude(self, vector):
        return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2 )
