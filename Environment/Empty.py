"""
This file contains the environment class called EmptyWorld.
This class is responsible for simulating the environment for the agents during training
"""


from random import randint
from Robots import Ally, Adversary
import math
import numpy as np

class EmptyWorld:
    def __init__(self, realWorld):
        self.n_agents = 3
        self.trueObs = []
        self.allies = []
        self.adv = Adversary.Adversary(4, realWorld)
        self.stepNum = 0
        self.maxIterations = 1000
        self.boundary = 1500
        for i in range(3):
            self.allies.append(Ally.Ally(i+1, realWorld))

        for ally in self.allies:
            ally.setup()
            ally.setAllies(self.allies)
            ally.setAdv(self.adv)

        self.adv.setup()
        self.adv.setAllies(self.allies)

    def reset(self):
        return self.getObservations()

    def getErroredPostion(self, ally, adv):
        distanceToOject = self.calcDistanceBetweenPoints(ally, adv)
        errorValue = (np.random.normal(distanceToOject, distanceToOject/10, 1)[0]) - distanceToOject
        return [adv[0] + errorValue, adv[1] + errorValue, adv[2] + errorValue]

    def getObservations(self):
        observations = []
        self.adv.calcStatus()
        for ally in self.allies:
            ally.calcStatus()
            advPos = self.getErroredPostion(ally.pos, self.adv.pos)
            observations.append((ally.pos[0],ally.pos[1],ally.pos[2],advPos[0],advPos[1],advPos[2]))
        self.getTrueObservations()
        return observations

    def getTrueObservations(self):
        observations = []
        self.adv.calcStatus()
        advPos = self.adv.pos
        for ally in self.allies:
            ally.calcStatus()
            observations.append((ally.pos[0],ally.pos[1],ally.pos[2],advPos[0],advPos[1],advPos[2]))
        self.trueObs = observations

    def getRewards(self, oldObs, newObs, actions):
        rewards = []
        advCenterOldDist = self.calcDistanceBetweenPoints([0,0,50],[oldObs[0][3], oldObs[0][4], oldObs[0][5]])
        advCenterNewDist = self.calcDistanceBetweenPoints([0,0,50],[newObs[0][3], newObs[0][4], newObs[0][5]])
        globalReward = advCenterNewDist - advCenterOldDist
        for i in range(self.n_agents):
            oldDist = self.calcDistanceBetweenPoints([oldObs[i][0], oldObs[i][1], oldObs[i][2]],[oldObs[i][3], oldObs[i][4], oldObs[i][5]])
            newDist = self.calcDistanceBetweenPoints([newObs[i][0], newObs[i][1], newObs[i][2]],[newObs[i][3], newObs[i][4], newObs[i][5]])
            reward = oldDist - newDist
            totalReward = reward + globalReward
            if advCenterNewDist >= self.boundary:
                totalReward += 5
            elif advCenterNewDist <= 100:
                totalReward -= 5
            rewards.append(totalReward)

        return rewards

    def isOutOfBounds(self, pos):
        refPoint = [0,0,50]
        dist = self.calcDistanceBetweenPoints(pos, refPoint)
        if dist > self.boundary:
            return True
        return False

    def calcDistanceBetweenPoints(self, selfPoint, refPoint):
        ans = 0
        for i in range(len(selfPoint)):
            ans += (selfPoint[i]-refPoint[i])**2
        return math.sqrt(ans)

    def getIsDone(self):
        if self.stepNum >= self.maxIterations:
            return True
        self.adv.calcStatus()
        advPos = self.adv.pos
        for ally in self.allies:
            ally.calcStatus()
            if self.isEqual(ally.pos,advPos):
                return True
        return self.isOutOfBounds(advPos)

    def isEqual(self, a, b):
        if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
            return True
        return False


    def step(self, actions):
        self.runAllies(actions)
        self.runAdv()
        self.stepNum +=1
        oldObs = self.trueObs
        _ = self.getObservations()
        newObs = self.trueObs
        return (newObs, self.getRewards(oldObs, newObs, actions), self.getIsDone())

    def runAllies(self, actions):
        i = 0
        for ally in self.allies:
            ally.calcWaypoints(self.decodeAction(actions[i]))
            ally.runMove()
            i += 1

    def runAdv(self):
        self.adv.calcWaypoints()
        self.adv.runMove()

    def printToFile(self, write):
        for ally in self.allies:
            ally.printHistory(write)
        self.adv.printHistory(write)

    def decodeAction(self, action):
        if action == 0:
            return [0,0,0]
        if action == 1:
            return [0,1,0]
        if action == 2:
            return [1,1,0]
        if action == 3:
            return [1,0,0]
        if action == 4:
            return [1,-1,0]
        if action == 5:
            return [0,-1,0]
        if action == 6:
            return [-1,-1,0]
        if action == 7:
            return [-1,0,0]
        if action == 8:
            return [-1,1,0]
        if action == 9:
            return [0,0,1]
        if action == 10:
            return [0,1,1]
        if action == 11:
            return [1,1,1]
        if action == 12:
            return [1,0,1]
        if action == 13:
            return [1,-1,1]
        if action == 14:
            return [0,-1,1]
        if action == 15:
            return [-1,-1,1]
        if action == 16:
            return [-1,0,1]
        if action == 17:
            return [-1,1,1]
        if action == 18:
            return [0,0,-1]
        if action == 19:
            return [0,1,-1]
        if action == 20:
            return [1,1,-1]
        if action == 21:
            return [1,0,-1]
        if action == 22:
            return [1,-1,-1]
        if action == 23:
            return [0,-1,-1]
        if action == 24:
            return [-1,-1,-1]
        if action == 25:
            return [-1,0,-1]
        if action == 26:
            return [-1,1,-1]
