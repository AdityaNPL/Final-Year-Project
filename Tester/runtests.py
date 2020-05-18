import RobotTester as rt
import matplotlib.pyplot as plt

def runTest():
    robots = 3
    adv = 4
    los = 0
    br = 0
    angle = 0
    acc = 0
    globalTime = 0
    globalDist = 0
    for i in range(1,robots+1):
        roboTest = rt.RobotTester("./DataDump/data_"+str(i)+".csv", "./DataDump/data_adv"+str(adv)+".csv")
        roboTest.getDetailsFromFile()

        globalTime = roboTest.timeTakenToCapture()
        globalDist = roboTest.avgDistFromCenter()

        res1 = roboTest.countLineOfSight()
        print("Line of Sight")
        print(res1)
        print((res1[0] * 1.00)/res1[1])
        los += (res1[0] * 1.00)/res1[1]

        res2 = roboTest.countBlastRange()
        print("Blast Range")
        print(res2)
        print((res2[0] * 1.00)/res2[1])
        br +=(res2[0] * 1.00)/res2[1]

        res3 = roboTest.changeOfAngleOfSelf()
        print("Change in Angle -- see graph")
        print("Avg Change in Angle")
        avgChangeInAngle = sum(res3)/len(res3)
        print(avgChangeInAngle)
        angle += avgChangeInAngle

        res5 = roboTest.angularAcceleration()
        print("Angular Acceleration -- see graph")
        print(res5[len(res5)-1])
        print("Avg Angular Acceleration")
        avgAngularAcc = sum(res5)/len(res5)
        print(avgAngularAcc)
        acc += avgAngularAcc

        if i == 1:
            labelsAngle = range(1,len(res3)+1)
            valAngle = res3
            fig = plt.figure(figsize=(14, 7))
            axAngle = fig.add_subplot(121)
            axAngle.plot(labelsAngle,valAngle)
            axAngle.set_title("Change of Angle over Time")
            axAngle.set_ylabel("Change of Angle")
            axAngle.set_xlabel("Timestamp")

            labelsW = range(1,len(res5)+1)
            valW = res5
            axW = fig.add_subplot(122)
            axW.plot(labelsW,valW)
            axW.set_title("Angular Acceleration over Time")
            axW.set_ylabel("Angular Acc")
            axW.set_xlabel("Timestamp")
            plt.tight_layout()
            plt.show()
            # print(res6)

    print("######Final#######")
    print(globalTime)
    print("%.2f" % ((los/robots)*100.00))
    print("%.2f" % ((br/robots)*100.00))
    print("%.1f" % (globalDist))
    print("%.4f" % (angle/robots))
    print("%.4f" % (acc/robots))
