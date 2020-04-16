import RobotTester as rt
import matplotlib.pyplot as plt

roboTest = rt.RobotTester("./DataDump/data_3.csv", "./DataDump/data_adv5.csv")
roboTest.getDetailsFromFile()

res = roboTest.timeTakenToCapture()
print("Time Taken")
print(res)

res1 = roboTest.countLineOfSight()
print("Line of Sight")
print(res1)

res2 = roboTest.countBlastRange()
print("Blast Range")
print(res2)

res3 = roboTest.rateOfChangeOfAngleOfSelf()
res4 = roboTest.timeViewChangeOfAngleOfSelf()
print("Rate of Change of Angle (running average) -- see graph")
# print(res4)

res5 = roboTest.avgAngularAcleration()
res6 = roboTest.timeViewAngularAcleration()
print("Angular Acceleration (running average)")

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
axW.set_xlabel("Turn number")
plt.tight_layout()
plt.show()
# print(res6)
