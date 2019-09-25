import math


class AdversaryRobotClass:

    def __init__(self, pos_x, pos_y, grid_ui_obj):
        self.init_x = pos_x
        self.init_y = pos_y
        self.move_x = 0
        self.move_y = 0
        self.vel = 10
        self.size = 20
        self.direction = 0
        self.grid_ui_obj = grid_ui_obj
        self.rectangle = self.grid_ui_obj.canvas.create_rectangle(self.init_x, self.init_y,
                                                                  self.init_x+self.size, self.init_y+self.size,
                                                                  fill="red")

    '''
    Direction = [0,359] => anti-clockwise angle from horizontal 
    '''
    def change_direction_to(self, speed, direction):
        self.move_x = math.ceil(speed*math.cos(math.radians(direction)))
        self.move_y = math.ceil(speed*math.sin(math.radians(direction)))

    def move(self):
        self.change_direction_to(self.vel, self.direction)
        self.direction = self.direction + 10
        if self.direction >= 360:
            self.direction = self.direction - 360

        self.grid_ui_obj.canvas.move(self.rectangle, self.move_x, self.move_y)

        self.grid_ui_obj.canvas.after(50, self.move)
