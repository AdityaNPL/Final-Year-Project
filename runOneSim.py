from EAsim import EAsim

genes = {"iterations":683, "maxSpeed":87, "decreasingVal":81}
sim = EAsim.EAsim(genes)
sim.run()
sim.printToFile(True)
