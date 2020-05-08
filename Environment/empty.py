from random import randint
from Robots import Ally,Adversary

class EmptyWorld:
    def __init__(self):
        self.n_agents = 3
        self.allies = []
        self.adv = Adversary.Adversary(4, False)
        self.step = 0
        self.maxIterations = 100
        for i in range(3):
            self.allies.append(Ally.Ally(i+1, False))

        for ally in self.allies:
            ally.setup()
            ally.setAllies(self.allies)
            ally.setAdv(self.adv)

        self.adv.setup()
        self.adv.setAllies(self.allies)

    def reset(self):
        return self.getObservations()

    def getObservations(self):
        observations = []
        self.adv.calcStatus()
        advPos = self.adv.pos
        for ally in self.allies:
            ally.calcStatus()
            observations.append((ally.pos[0],ally.pos[1],ally.pos[2],advPos[0],advPos[1],advPos[2]))
        return observations

    def getRewards(self):
        rewards = []
        for ally in self.allies:
            rewards.append(randint(-10, 10))
        return rewards

    def getIsDone(self):
        if self.step >= self.maxIterations:
            return True
        self.adv.calcStatus()
        advPos = self.adv.pos
        for ally in self.allies:
            ally.calcStatus()
            if self.isEqual(ally.pos,advPos):
                return True
        return False

    def isEqual(self, a, b):
        if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
            return True
        return False


    def step(self, actions):
        self.runAllies(actions)
        self.runAdv()
        self.step +=1
        return (self.getObservations(), self.getRewards(), self.getIsDone())

    def runAllies(self, actions):
        i = 0
        for ally in self.allies:
            ally.calcWaypoints(self.decodeAction(actions[i]))
            ally.runMove()
            i += 1

    def runAdv(self):
        self.adv.calcWaypoints()
        self.adv.runMove()

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
