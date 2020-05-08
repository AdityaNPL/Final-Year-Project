class EmptyWorld:
    def __init__(self):
        self.robots = 3
        pass

    def getObservations(self):
        observations = []
        for ally in self.allie:
            ally.calcStatus()
            observations.append(ally.pos)
        return observations

    def getRewards(self):
        pass

    def getIsDone(self):
        pass

    def step(self, actions):
        self.runAllies(actions)
        self.runAdv()
        return (self.getObservations(), self.getRewards(), self.getIsDone())
