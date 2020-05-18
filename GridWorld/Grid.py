"""
This file contains the class for Grid.
This class is responsible for the grid world attribute of the simulation.
"""

from UI import GridUI
import Adversary, Ally


class GridClass:

    grid_width = 1300
    grid_height = 700

    def __init__(self):
        self.grid_ui_obj = GridUI.GridUIClass(self.grid_width, self.grid_height)

        self.adv = Adversary.AdversaryRobotClass(0, 0, self.grid_ui_obj, "adv1")
        self.ally1 = Ally.AllyRobotClass(0, 350, self.grid_ui_obj, "1")
        self.ally2 = Ally.AllyRobotClass(650, 700, self.grid_ui_obj, "2")
        self.ally3 = Ally.AllyRobotClass(1300, 350, self.grid_ui_obj, "3")

        self.adv.set_opponent_details([self.ally1, self.ally2, self.ally3])
        self.ally1.set_opponent_details(self.adv)
        self.ally2.set_opponent_details(self.adv)
        self.ally3.set_opponent_details(self.adv)

        self.ally1.set_ally_details([self.ally2, self.ally3])
        self.ally2.set_ally_details([self.ally1, self.ally3])
        self.ally3.set_ally_details([self.ally1, self.ally2])

        self.adv.move()
        self.ally1.move()
        self.ally2.move()
        self.ally3.move()

        self.run_ui_loop()

    def run_ui_loop(self):
        self.grid_ui_obj.run_main_loop()
