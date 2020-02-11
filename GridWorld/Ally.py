import math
import Robot


class AllyRobotClass(Robot.RobotClass):

    def __init__(self, pos_x, pos_y, grid_ui_obj, labeltxt):
        Robot.RobotClass.__init__(self, pos_x, pos_y, grid_ui_obj)
        self.rectangle = self.grid_ui_obj.canvas.create_rectangle(self.pos_x, self.pos_y,
                                                                  self.pos_x + self.size, self.pos_y + self.size,
                                                                  fill="blue")
        self.label_txt = labeltxt
        self.label = self.grid_ui_obj.canvas.create_text((self.pos_x, self.pos_y), text=labeltxt)
        self.force_const = 500000


    def set_ally_details(self, listOfAlly):
        self.ally_details = []
        for ally in listOfAlly:
            self.ally_details.append(ally)

    def move(self):

        next_dir = self.get_best_dir()
        self.change_direction_to(next_dir)
        self.update_position()
        if not self.opponent_details.stop:
            self.grid_ui_obj.canvas.move(self.rectangle, self.speed_x, self.speed_y)
            self.grid_ui_obj.canvas.move(self.label, self.speed_x, self.speed_y)
            self.grid_ui_obj.canvas.after(self.step_delay_rate, self.move)

    def get_best_dir(self):
        opponent_x = self.opponent_details.pos_x
        opponent_y = self.opponent_details.pos_y
        direction = self.get_direction_to_object(self.pos_x, self.pos_y, opponent_x, opponent_y)
        direction = math.radians(direction)

        # Force towards is proportional to the distance to the opponent
        force_towards = self.get_distance_to_object(self.pos_x, self.pos_y, opponent_x, opponent_y)
        v1 = [force_towards*math.cos(direction), force_towards*math.sin(direction)]
        # print("to: " + str(force_towards))

        for ally in self.ally_details:
            dir_away = self.get_dir_away_from_object(ally.pos_x, ally.pos_y, self.pos_x, self.pos_y)
            distance_to = self.get_distance_to_object(ally.pos_x, ally.pos_y, self.pos_x, self.pos_y)
            dir_away = math.radians(dir_away)

            # Force away is proportional to the 1 / distance^2 to the opponent
            force_away = self.force_const/(distance_to*distance_to)
            # print("away " + str(force_away) + " dist " + str(distance_to))
            v2 = [force_away*math.cos(dir_away), force_away*math.sin(dir_away)]
            v1[0] += v2[0]
            v1[1] += v2[1]

        direction = math.degrees(math.atan2(v1[1], v1[0]))

        if not self.force_const<10000:
            self.force_const -= 1000

        print(self.force_const)
        return direction

