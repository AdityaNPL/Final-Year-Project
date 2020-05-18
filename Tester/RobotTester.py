"""
This file contains the class for the RobotTester.
This class is responsible for testing the results of the simulation by calculating the perfromance metrics.
"""

import os
import csv
import math
class RobotTester:
    def __init__(self, selfFile, oppFile):
        self.selfFile = selfFile
        self.oppFile = oppFile
        self.selfPos = []
        self.selfSpeed = []
        self.oppPos = []
        self.oppSpeed = []

        if isinstance(selfFile, list):
            self.selfPos = selfFile[0]
            self.oppPos = oppFile[0]
            self.selfSpeed = selfFile[1]
            self.oppSpeed = oppFile[1]

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
                self.selfPos.append((float(row[1]), float(row[2]), float(row[3])))
                self.selfSpeed.append((float(row[4]), float(row[5]), float(row[6])))

        with open(self.oppFile, "r") as f:
            data = csv.reader(f, delimiter=',', quotechar='|')
            colNames = True
            for row in data:
                if colNames:
                    colNames = False
                    continue
                self.oppPos.append((float(row[1]), float(row[2]), float(row[3])))
                self.oppSpeed.append((float(row[4]), float(row[5]), float(row[6])))


    def countLineOfSight(self):
        count = 0
        for time in range(len(self.selfPos)):
            thetaX = self.calcAngleX(self.selfPos[time], self.oppPos[time])
            phiX = self.calcAngleX(self.selfSpeed[time], (0,0,0)) # angle to horizontal based on speed vectors for direction
            thetaY = self.calcAngleY(self.selfPos[time], self.oppPos[time])
            phiY = self.calcAngleY(self.selfSpeed[time], (0,0,0)) # angle to horizontal based on speed vectors for direction
            thetaZ = self.calcAngleZ(self.selfPos[time], self.oppPos[time])
            phiZ = self.calcAngleZ(self.selfSpeed[time], (0,0,0)) # angle to horizontal based on speed vectors for direction

            if abs(thetaX - phiX) < self.lineOfSight and abs(thetaY - phiY) < self.lineOfSight and abs(thetaZ - phiZ) < self.lineOfSight:
                count += 1
        return (count, len(self.selfPos))


    def calcAngleX(self, selfPoint, refPoint):
        magYZ = self.calcDistanceBetweenPoints([selfPoint[1], selfPoint[2]], [refPoint[1], refPoint[2]])
        if (magYZ == 0):
            return 90
        tanVal = (refPoint[2] - selfPoint[2])/(magYZ)
        return math.degrees(math.atan(tanVal))

    def calcAngleY(self, selfPoint, refPoint):
        magXZ = self.calcDistanceBetweenPoints([selfPoint[0], selfPoint[2]], [refPoint[0], refPoint[2]])
        if (magXZ == 0):
            return 90
        tanVal = (refPoint[2] - selfPoint[2])/(magXZ)
        return math.degrees(math.atan(tanVal))

    def calcAngleZ(self, selfPoint, refPoint):
        magXY = self.calcDistanceBetweenPoints([selfPoint[0], selfPoint[1]], [refPoint[0], refPoint[1]])
        if (magXY == 0):
            return 90
        tanVal = (refPoint[2] - selfPoint[2])/(magXY)
        return math.degrees(math.atan(tanVal))

    def calcDistanceBetweenPoints(self, selfPoint, refPoint):
        ans = 0
        for i in range(len(selfPoint)):
            ans += (selfPoint[i]-refPoint[i])**2
        return math.sqrt(ans)

    def countBlastRange(self):
        count = 0
        for time in range(len(self.selfPos)):
            if abs(self.oppPos[time][0] - self.selfPos[time][0]) < self.blastRange and abs(self.oppPos[time][1] - self.selfPos[time][1]) < self.blastRange and abs(self.oppPos[time][2] - self.selfPos[time][2]) < self.blastRange:
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
                    if (radiusOfTurn == 0):
                        accOverTime.append(0)
                        continue
                    angularAcc = angularVel / radiusOfTurn
                    accOverTime.append(angularAcc)
        return accOverTime

    def timeTakenToCapture(self):
        return len(self.oppPos)

    def anglesWithTime(self):
        listOfAngles = []
        for time in range(len(self.selfSpeed)):
            currentAngleX = self.calcAngleX(self.selfSpeed[time], (0,0,0))
            currentAngleY = self.calcAngleY(self.selfSpeed[time], (0,0,0))
            currentAngleZ = self.calcAngleZ(self.selfSpeed[time], (0,0,0))
            currentAngle = (currentAngleX + currentAngleY + currentAngleZ) / 3
            listOfAngles.append((time,currentAngle))
        return listOfAngles

    def avgDistFromCenter(self):
        dist = 0
        for pos in self.oppPos:
            dist += self.calcDistanceBetweenPoints(pos,(0,0,50))
        return (dist * 1.0)/len(self.oppPos)
