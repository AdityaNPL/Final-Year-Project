from Tkinter import *


class GridUIClass:

    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.window = Tk()
        self.window.title("Grid World")
        self.canvas = Canvas(self.window, width=self.grid_width, height=self.grid_height)
        self.canvas.pack()

    def run_main_loop(self):
        self.window.mainloop()
