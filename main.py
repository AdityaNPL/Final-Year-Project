import Ally

allies = []
print("Started")
for i in range(3):
	allies.append(Ally.Ally(i+1,20))
	allies[i].setup()

print("setup")

for i in range(20):
	for j in range(3):
		allies[j].encircle([0,0,0])

for i in range(3):
	allies[i].printStatus()
