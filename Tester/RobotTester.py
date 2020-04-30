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
        valuesOverTime.append((0,0))
        accForEachTurn = []
        startPos = 0
        for pos in range(len(valuesOverTime)-1):
            if valuesOverTime[pos][0] + 1 != valuesOverTime[pos+1][0]:
                time = valuesOverTime[pos][0] - valuesOverTime[startPos][0]
                if time == 0:
                    continue
                changeInAngle = math.radians(abs(valuesOverTime[pos][1] - valuesOverTime[startPos][1]))
                angularVel = changeInAngle/time
                distanceBetweenPoints = self.calcDistanceBetweenPoints(self.selfPos[valuesOverTime[pos][0]],self.selfPos[valuesOverTime[startPos][0]])
                radiusOfTurn = (distanceBetweenPoints/2)/(math.sin(changeInAngle/2))
                angularAcc = angularVel / radiusOfTurn
                accForEachTurn.append(angularAcc)
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
            currentAngle = self.calcAngle(self.selfSpeed[time],(0,0))
            nextAngle = self.calcAngle(self.selfSpeed[time+1],(0,0))
            listOfTimes.append((time,abs(currentAngle - nextAngle)))
        return listOfTimes

    def timeViewAngularAcleration(self):
        listOfTimes = []
        for time in range(len(self.selfPos)):
            currentAngle = self.calcAngle(self.selfSpeed[time],(0,0))
            if len(listOfTimes) == 0 or currentAngle != listOfTimes[len(listOfTimes)-1][1]:
                listOfTimes.append((time,currentAngle))
        return listOfTimes

    def avgDistFromCenter(self):
        dist = 0
        for pos in self.oppPos:
            dist += self.calcDistanceBetweenPoints(pos,(650,350))
            # print(self.calcDistanceBetweenPoints(pos,(650,350)))
        return (dist * 1.0)/len(self.oppPos)
