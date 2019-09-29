import math
import Robot


class AllyRobotClass(Robot.RobotClass):

    def __init__(self, pos_x, pos_y, grid_ui_obj):
        Robot.RobotClass.__init__(self, pos_x, pos_y, grid_ui_obj)
        self.rectangle = self.grid_ui_obj.canvas.create_rectangle(self.pos_x, self.pos_y,
                                                                  self.pos_x + self.size, self.pos_y + self.size,
                                                                  fill="blue")

    def move(self):
        print self.grid_ui_obj.grid_width
        direction = self.direction
        if self.pos_x > self.grid_ui_obj.grid_width:
            self.change_direction_to(self.speed, 180)
        elif self.pos_x < 0:
            self.change_direction_to(self.speed, 0)
        else:
            self.change_direction_to(self.speed, direction)

        self.grid_ui_obj.canvas.move(self.rectangle, self.move_x, self.move_y)
        self.grid_ui_obj.canvas.after(50, self.move)
