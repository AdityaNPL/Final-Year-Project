"""
This file contains the class for GridUI.
This class is responsible for the UI visualisation and rendering of the simulation.
"""

from Tkinter import *
import math

class GridUIClass:

    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_diagonal = math.sqrt(math.pow(self.grid_height, 2) + math.pow(self.grid_width, 2))
        self.window = Tk()
        self.window.title("Grid World")
        self.canvas = Canvas(self.window, width=self.grid_width, height=self.grid_height)
        self.canvas.pack()

    def run_main_loop(self):
        self.window.mainloop()
