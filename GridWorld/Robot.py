import math
import abc


class RobotClass:

    def __init__(self, pos_x, pos_y, grid_ui_obj):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.move_x = 0
        self.move_y = 0
        self.speed = 10
        self.size = 20
        self.direction = 0
        self.grid_ui_obj = grid_ui_obj
        self.rectangle = None
        self.opponent_details = None

    '''
    Direction = [0,359] => anti-clockwise angle from horizontal 
    '''
    def change_direction_to(self, speed, direction):
        self.speed = speed
        self.direction = direction
        self.move_x = math.ceil(self.speed*math.cos(math.radians(self.direction)))
        self.move_y = math.ceil(self.speed*math.sin(math.radians(self.direction)))
        self.pos_x += self.move_x
        self.pos_y += self.move_y

    def set_opponent_details(self, opponent_details):
        self.opponent_details = opponent_details

    @abc.abstractmethod
    def move(self):
        pass
