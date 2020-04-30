from EAsim import EAsim
from random import randint
import matplotlib.pyplot as plt

minIterations=100
maxIterations=1000
minSpeed=1
MaxSpeed=100
minDecreasing=1
MaxDecreasing=100

initialPop = 100
population = []
oldPopulation = []
fitnessVal = 50
fitnessHistory = []
populationHistory = []

def getChildren(parents):
    c1 = {"iterations":parents[randint(0, 1)]["iterations"], "maxSpeed":parents[randint(0, 1)]["maxSpeed"], "decreasingVal":parents[randint(0, 1)]["decreasingVal"]}
    c2 = {"iterations":parents[randint(0, 1)]["iterations"], "maxSpeed":parents[randint(0, 1)]["maxSpeed"], "decreasingVal":parents[randint(0, 1)]["decreasingVal"]}
    # Mutate C1 1/10
    if randint(0,100)%47 == 0 :
        c1["iterations"] = mutate(c1["iterations"], minIterations,maxIterations)
        c1["maxSpeed"] = mutate(c1["maxSpeed"], minSpeed, MaxSpeed)
        c1["decreasingVal"] = mutate(c1["decreasingVal"], minDecreasing, MaxDecreasing)
    if randint(0,100)%47 == 0 :
        c2["iterations"] = mutate(c2["iterations"], minIterations,maxIterations)
        c2["maxSpeed"] = mutate(c2["maxSpeed"], minSpeed, MaxSpeed)
        c2["decreasingVal"] = mutate(c2["decreasingVal"], minDecreasing, MaxDecreasing)
    return c1,c2
def mutate(val, min, max):
    if randint(0,100)%47 == 0:
        print("mutate")
        return randint(min,max)
    else:
        return val


for i in range(initialPop):
    genes = {"iterations":randint(minIterations, maxIterations), "maxSpeed":randint(minSpeed, MaxSpeed), "decreasingVal":randint(minDecreasing, MaxDecreasing)}
    population.append(EAsim.EAsim(genes))

while fitnessVal < 100 and len(population) > 1:
    print(len(population), fitnessVal)
    populationHistory.append(len(population))
    if(len(population) < 5):
        for r in population:
            print(r.genes)

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

    if len(newPopulation) >= len(population):
        if fitnessVal >= 60:
            fitnessVal += 0.5
        elif fitnessVal >= 55 :
            fitnessVal += 1
        else:
            fitnessVal += 3

    oldPopulation = population
    population = newPopulation

print(fitnessHistory)
print(populationHistory)
print(list(map(lambda x: x.genes, oldPopulation)))

fig = plt.figure(figsize=(14, 7))
axFitness = fig.add_subplot(121)
axFitness.plot(range(1,len(fitnessHistory)+1),fitnessHistory)
axFitness.set_title("Fitness over Run")
axFitness.set_ylabel("Fitness")
axFitness.set_xlabel("Run")

axPopulation = fig.add_subplot(122)
axPopulation.plot(range(1,len(populationHistory)+1),populationHistory)
axPopulation.set_title("Population over Run")
axPopulation.set_ylabel("Population")
axPopulation.set_xlabel("Run")
plt.tight_layout()
plt.show()
