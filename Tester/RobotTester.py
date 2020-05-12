import os
import csv
import math
class RobotTester:
    def __init__(self, selfFile, oppFile):
        self.selfFile = selfFile
        self.oppFile = oppFile
        self.selfPos = []
        self.oppPos = []
        self.selfSpeed = []
        self.oppSpeed = []
        self.lineOfSight = 15 # in degrees
        self.blastRange = 100

    def getDetailsFromFile(self):
        self.selfPos = []
        self.selfSpeed = []
        self.oppPos = []
        self.oppSpeed = []
        with open(self.selfFile, "r") as f:
            data = csv.reader(f, delimiter=',', quotechar='|')
            colNames = True
            for row in data:
                if colNames:
                    colNames = False
                    continue
                self.selfPos.append((float(row[1]), float(row[2])))
                self.selfSpeed.append((float(row[3]), float(row[4])))

        with open(self.oppFile, "r") as f:
            data = csv.reader(f, delimiter=',', quotechar='|')
            colNames = True
            for row in data:
                if colNames:
                    colNames = False
                    continue
                self.oppPos.append((float(row[1]), float(row[2])))
                self.oppSpeed.append((float(row[3]), float(row[4])))


    def countLineOfSight(self):
        count = 0
        for time in range(len(self.selfPos)):
            theta = self.calcAngle(self.selfPos[time], self.oppPos[time])
            phi = self.calcAngle(self.selfSpeed[time], (0,0)) # angle to horizontal based on speed vectors for direction
            if abs(theta - phi) < self.lineOfSight:
                count += 1
        return (count, len(self.selfPos))

    def calcAngle(self, selfPoint, refPoint):
        denom = (refPoint[0] - selfPoint[0])
        if (denom == 0):
            return 90
        tanVal = (refPoint[1] - selfPoint[1])/denom
        return math.degrees(math.atan(tanVal))

    def calcDistanceBetweenPoints(self, selfPoint, refPoint):
        return math.sqrt( ((selfPoint[0]-refPoint[0])**2)+((selfPoint[1]-refPoint[1])**2) )

    def countBlastRange(self):
        count = 0
        for time in range(len(self.selfPos)):
            if abs(self.oppPos[time][0] - self.selfPos[time][0]) < self.blastRange and abs(self.oppPos[time][1] - self.selfPos[time][1]) < self.blastRange:
                count += 1
        return (count, len(self.selfPos))

    def changeOfAngleOfSelf(self):
        valuesOverTime = self.anglesWithTime()
        angleChangeOverTime = []
        for time in range(len(valuesOverTime)):
            if time == 1:
                angleChangeOverTime.append(0)
            else:
                angleChange = math.radians(abs(valuesOverTime[time][1] - valuesOverTime[time-1][1]))
                angleChangeOverTime.append(angleChange)
        return angleChangeOverTime


    def angularAcceleration(self):
        valuesOverTime = self.anglesWithTime()
        accOverTime = []
        for time in range(len(valuesOverTime)):
            if time == 1:
                accOverTime.append(0)
            else:
                angularVel = math.radians(abs(valuesOverTime[time][1] - valuesOverTime[time-1][1]))
                if (angularVel == 0):
                    accOverTime.append(0)
                else:
                    distanceBetweenPoints = self.calcDistanceBetweenPoints(self.selfPos[time],self.selfPos[time-1])
                    radiusOfTurn = (distanceBetweenPoints/2)/(math.sin(angularVel/2))
                    angularAcc = angularVel / radiusOfTurn
                    accOverTime.append(angularAcc)
        return accOverTime

    def timeTakenToCapture(self):
        return len(self.oppPos)

    def anglesWithTime(self):
        listOfAngles = []
        for time in range(len(self.selfSpeed)):
            currentAngle = self.calcAngle(self.selfSpeed[time],(0,0))
            listOfAngles.append((time,currentAngle))
        return listOfAngles

    def avgDistFromCenter(self):
        dist = 0
        for pos in self.oppPos:
            dist += self.calcDistanceBetweenPoints(pos,(650,350))
            # print(self.calcDistanceBetweenPoints(pos,(650,350)))
        return (dist * 1.0)/len(self.oppPos)
