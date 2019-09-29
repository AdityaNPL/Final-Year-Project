import math
import Robot


class AdversaryRobotClass(Robot.RobotClass):

    def __init__(self, pos_x, pos_y, grid_ui_obj):
        Robot.RobotClass.__init__(self, pos_x, pos_y, grid_ui_obj)
        self.rectangle = self.grid_ui_obj.canvas.create_rectangle(self.pos_x, self.pos_y,
                                                                  self.pos_x+self.size, self.pos_y+self.size,
                                                                  fill="red")

    def move(self):
        direction = self.direction
        self.change_direction_to(self.speed, direction + 10)
        if direction >= 360:
            self.direction = direction - 360

        self.grid_ui_obj.canvas.move(self.rectangle, self.move_x, self.move_y)

        self.grid_ui_obj.canvas.after(50, self.move)
