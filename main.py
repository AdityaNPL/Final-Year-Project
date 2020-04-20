from EAsim import EAsim
from random import randint


def getChildren(parents):
    c1 = {"iterations":parents[randint(0, 1)]["iterations"], "maxSpeed":parents[randint(0, 1)]["maxSpeed"], "decreasingVal":parents[randint(0, 1)]["decreasingVal"]}
    c2 = {"iterations":parents[randint(0, 1)]["iterations"], "maxSpeed":parents[randint(0, 1)]["maxSpeed"], "decreasingVal":parents[randint(0, 1)]["decreasingVal"]}
    # Mutate C1 1/10
    if randint(0,100)%47 == 0 :
        c1["iterations"] = mutate(c1["iterations"], 100,1000)
        c1["maxSpeed"] = mutate(c1["maxSpeed"], 1, 10)
        c1["decreasingVal"] = mutate(c1["decreasingVal"], 1, 10)
    if randint(0,100)%47 == 0 :
        c2["iterations"] = mutate(c2["iterations"], 100,1000)
        c2["maxSpeed"] = mutate(c2["maxSpeed"], 1, 10)
        c2["decreasingVal"] = mutate(c2["decreasingVal"], 1, 10)
    return c1,c2
def mutate(val, min, max):
    if randint(0,100)%47 == 0:
        print("mutate")
        return randint(min,max)
    else:
        return val



initialPop = 100
population = []
fitnessVal = 1
fitnessHistory = []

for i in range(initialPop):
    genes = {"iterations":randint(100, 1000), "maxSpeed":randint(1, 10), "decreasingVal":randint(1, 10)}
    population.append(EAsim.EAsim(genes))

while fitnessVal < 100 and len(population) >= 1:
    print(len(population), fitnessVal)
    parents = []
    sumFit = 0
    for sim in population:
        sim.run()
        fit = sim.fitness()
        sumFit += fit
        if fit > fitnessVal:
            parents.append(sim.genes)

    fitnessHistory.append(sumFit/len(population))

    newPopulation = []

    for i in range(0,len(parents)-1,2):
        newPopulation.append(EAsim.EAsim(parents[i]))
        newPopulation.append(EAsim.EAsim(parents[i+1]))
        child1, child2 = getChildren([parents[i],parents[i+1]])
        newPopulation.append(EAsim.EAsim(child1))
        newPopulation.append(EAsim.EAsim(child2))
    if len(parents)%2 == 1:
        newPopulation.append(EAsim.EAsim(parents[len(parents)-1]))
        child1, child2 = getChildren([parents[0], parents[len(parents)-1]])
        newPopulation.append(EAsim.EAsim(child1))
        newPopulation.append(EAsim.EAsim(child2))

    population = newPopulation
    fitnessVal += 1

print(fitnessHistory)
