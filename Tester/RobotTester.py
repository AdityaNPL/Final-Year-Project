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
        self.blastRange = 50

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

    def rateOfChangeOfAngleOfSelf(self):
        valuesOverTime = self.timeViewChangeOfAngleOfSelf()
        sumofValues = 0
        avgOverTime = []
        counter = 0
        for val in valuesOverTime:
            sumofValues += val[1]
            counter += 1
            avgOverTime.append((counter,sumofValues/counter))
        return avgOverTime

    def avgAngularAcleration(self):
        valuesOverTime = self.timeViewAngularAcleration()
        valuesOverTime.append((0,0,0))
        accForEachTurn = []
        startPos = 0
        for pos in range(len(valuesOverTime)-1):
            if valuesOverTime[pos][0] + 1 != valuesOverTime[pos+1][0]:
                time = valuesOverTime[pos][0] - valuesOverTime[startPos][0]
                changeInAngle = math.radians(abs(valuesOverTime[pos][1] - valuesOverTime[startPos][1]))
                angularVel = changeInAngle/time
                distanceBetweenPoints = self.calcDistanceBetweenPoints(self.selfPos[valuesOverTime[pos][0]],self.selfPos[valuesOverTime[startPos][0]])
                if changeInAngle != 0:
                    radiusOfTurn = (distanceBetweenPoints/2)/(math.sin(changeInAngle/2))
                    angularAcc = angularVel / radiusOfTurn
                    accForEachTurn.append(angularAcc)
                else:
                    accForEachTurn.append(0)
                startPos = pos+1

        sumofValues = 0
        avgOverTime = []
        counter = 0
        for val in accForEachTurn:
            sumofValues += val
            counter += 1
            avgOverTime.append((counter,sumofValues/counter))
        return avgOverTime

    def timeTakenToCapture(self):
        return len(self.oppPos)

    def timeViewChangeOfAngleOfSelf(self):
        listOfTimes = []
        for time in range(len(self.selfPos)-1):
            currentAngleX = self.calcAngleX(self.selfSpeed[time], (0,0,0))
            currentAngleY = self.calcAngleY(self.selfSpeed[time], (0,0,0))
            currentAngleZ = self.calcAngleZ(self.selfSpeed[time], (0,0,0))
            nextAngleX = self.calcAngleX(self.selfSpeed[time+1],(0,0,0))
            nextAngleY = self.calcAngleY(self.selfSpeed[time+1],(0,0,0))
            nextAngleZ = self.calcAngleZ(self.selfSpeed[time+1],(0,0,0))
            currentAngle = (currentAngleX + currentAngleY + currentAngleZ) / 3
            nextAngle = (nextAngleX + nextAngleY + nextAngleZ) / 3
            listOfTimes.append((time,abs(currentAngle - nextAngle)))
        return listOfTimes

    def timeViewAngularAcleration(self):
        listOfTimes = []
        for time in range(len(self.selfPos)):
            currentAngleX = self.calcAngleX(self.selfSpeed[time], (0,0,0))
            currentAngleY = self.calcAngleY(self.selfSpeed[time], (0,0,0))
            currentAngleZ = self.calcAngleZ(self.selfSpeed[time], (0,0,0))
            currentAngle = (currentAngleX + currentAngleY + currentAngleZ) / 3
            if len(listOfTimes) == 0 or currentAngle != listOfTimes[len(listOfTimes)-1][1]:
                listOfTimes.append((time,currentAngle))
        return listOfTimes
