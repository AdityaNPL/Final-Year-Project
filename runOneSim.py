from EAsim import EAsim

genes = {"iterations": 1000, "maxSpeed": 5, "decreasingVal": 2}
sim = EAsim.EAsim(genes)
sim.run()
sim.printToFile(True)
