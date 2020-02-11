import math
import abc


class RobotClass:

    def __init__(self, pos_x, pos_y, grid_ui_obj):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed = 5
        self.acc_mag = 2
        self.acc_dir = 0
        self.size = 5
        self.grid_ui_obj = grid_ui_obj
        self.rectangle = None
        self.label = None
        self.opponent_details = None
        self.ally_details = None
        self.step_delay_rate = 10
        self.label_txt = ""
        self.stop = False

    '''
    Direction = [0,359] => anti-clockwise angle from horizontal 
    '''
    def change_direction_to(self, direction):

        self.acc_dir = direction
        acc_x = self.acc_mag * math.cos(math.radians(self.acc_dir))
        acc_y = self.acc_mag * math.sin(math.radians(self.acc_dir))

        self.speed_x += acc_x
        self.speed_y += acc_y

        if self.speed_x > self.max_speed:
            self.speed_x = self.max_speed
        elif self.speed_x < self.max_speed * -1:
            self.speed_x = self.max_speed * -1

        if self.speed_y > self.max_speed:
            self.speed_y = self.max_speed
        elif self.speed_y < self.max_speed * -1:
            self.speed_y = self.max_speed * -1

    def set_opponent_details(self, opponent_details):
        if isinstance(opponent_details, list):
            self.opponent_details = []
            for opponent in opponent_details:
                self.opponent_details.append(opponent)
        else:
            self.opponent_details = opponent_details

    def get_direction_to_object(self, x1, y1, x2, y2):
        return math.degrees(math.atan2((y2-y1), (x2-x1)))

    def get_distance_to_object(self, x1, y1, x2, y2):
        return math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))

    def get_dir_away_from_object(self, x1, y1, x2, y2):
        direction = self.get_direction_to_object(x1, y1, x2, y2)
        return direction

    def update_position(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y


    @abc.abstractmethod
    def move(self):
        pass
