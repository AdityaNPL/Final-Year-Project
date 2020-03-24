import Ally

allies = []
print("Started")
for i in range(3):
	allies.append(Ally.Ally(i+1,20))

print("setup")
for i in range(3):
	allies[i].setup()
    allies[i].setAllies(allies)

for i in range(20):
	for j in range(3):
		allies[j].encircle([0,0,5])
	

for i in range(3):
	allies[i].printHistory()
