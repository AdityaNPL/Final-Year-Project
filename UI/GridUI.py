from Tkinter import *


class GridUIClass:

    def __init__(self, grid_width, grid_height):
        self.window = Tk()
        self.window.title("Grid World")
        self.canvas = Canvas(self.window, width=grid_width, height=grid_height)
        self.canvas.pack()

    def run_main_loop(self):
        self.window.mainloop()
