from UI import GridUI
import Adversary
import time


class GridClass:

    grid_width = 1300
    grid_height = 700

    def __init__(self):
        self.grid_ui_obj = GridUI.GridUIClass(self.grid_width, self.grid_height)
        self.adv = Adversary.AdversaryRobotClass(600, 200, self.grid_ui_obj)
        self.adv.move()
        self.run_ui_loop()

    def run_ui_loop(self):
        self.grid_ui_obj.run_main_loop()

