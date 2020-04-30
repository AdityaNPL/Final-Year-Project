import RobotTester as rt
import matplotlib.pyplot as plt

robots = 3
adv = 1
los = 0
br = 0
angle = 0
acc = 0
for i in range(1,robots+1):
    roboTest = rt.RobotTester("./DataDump/data_"+str(i)+".csv", "./DataDump/data_adv"+str(adv)+".csv")
    roboTest.getDetailsFromFile()

    res = roboTest.timeTakenToCapture()
    print("Time Taken")
    print(res)

    print("avg Dist")
    print(roboTest.avgDistFromCenter())

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

    res3 = roboTest.rateOfChangeOfAngleOfSelf()
    res4 = roboTest.timeViewChangeOfAngleOfSelf()
    print("Rate of Change of Angle (running average) -- see graph")
    print(res3[len(res3)-1])
    angle += res3[len(res3)-1][1]

    res5 = roboTest.avgAngularAcleration()
    res6 = roboTest.timeViewAngularAcleration()
    print("Angular Acceleration (running average)")
    print(res5[len(res5)-1])
    acc += res5[len(res5)-1][1]

    if i == 1:
        labelsAngle = []
        valAngle = []
        for val in res3:
            labelsAngle.append(val[0])
            valAngle.append(val[1])

        fig = plt.figure(figsize=(14, 7))
        axAngle = fig.add_subplot(121)
        axAngle.plot(labelsAngle,valAngle)
        axAngle.set_title("Rate of Change of Angle (running average)")
        axAngle.set_ylabel("Avg Rate of Change of Angle")
        axAngle.set_xlabel("Timestamp")

        labelsW = []
        valW = []
        for val in res5:
            labelsW.append(val[0])
            valW.append(val[1])

        axW = fig.add_subplot(122)
        axW.plot(labelsW,valW)
        axW.set_title("Angular Acceleration (running average)")
        axW.set_ylabel("Avg Angular Acc")
        axW.set_xlabel("Turn Number")
        plt.tight_layout()
        plt.show()
        # print(res6)

print("######Final#######")
print(los/robots)
print(br/robots)
print(angle/robots)
print(acc/robots)
