from UI import GridUI
import Adversary, Ally
import time


class GridClass:

    grid_width = 1300
    grid_height = 700

    def __init__(self):
        self.grid_ui_obj = GridUI.GridUIClass(self.grid_width, self.grid_height)
        self.adv = Adversary.AdversaryRobotClass(600, 200, self.grid_ui_obj)
        self.ally1 = Ally.AllyRobotClass(600, 150, self.grid_ui_obj)
        self.adv.set_opponent_details(self.ally1)
        self.ally1.set_opponent_details(self.adv)
        self.adv.move()
        self.ally1.move()
        self.run_ui_loop()

    def run_ui_loop(self):
        self.grid_ui_obj.run_main_loop()

