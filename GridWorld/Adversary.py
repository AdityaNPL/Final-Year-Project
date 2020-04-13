import math
import Robot
import time


class AdversaryRobotClass(Robot.RobotClass):

    def __init__(self, pos_x, pos_y, grid_ui_obj, label_txt):
        Robot.RobotClass.__init__(self, pos_x, pos_y, grid_ui_obj, label_txt)
        self.rectangle = self.grid_ui_obj.canvas.create_rectangle(self.pos_x, self.pos_y,
                                                                  self.pos_x+self.size, self.pos_y+self.size,
                                                                  fill="red")
        self.label = self.grid_ui_obj.canvas.create_text((self.pos_x, self.pos_y), text=label_txt)
        self.timer_start = time.time()
        self.timer_end = time.time()
        self.no_of_move_calls = 0
        self.grid_distribution = [[0 for i in range(self.grid_ui_obj.grid_width/100+1)] for j in range(self.grid_ui_obj.grid_height/100+1)]
        self.avgDistFromCenter = 0

    def move(self):
        self.no_of_move_calls += 1
        direction = self.get_best_possible_direction()
        self.change_direction_to(direction)
        if not self.stop:
            self.update_position()
            self.grid_distribution[int(self.pos_y/100)][int(self.pos_x/100)] += 1
            self.avgDistFromCenter += self.get_distance_to_object(self.grid_ui_obj.grid_width/2, self.pos_x, self.grid_ui_obj.grid_height/2, self.pos_y)
            self.grid_ui_obj.canvas.move(self.rectangle, self.speed_x, self.speed_y)
            self.grid_ui_obj.canvas.move(self.label, self.speed_x, self.speed_y)
            self.is_collided(self.pos_x, self.pos_y, self.size, self.opponent_details)
            self.grid_ui_obj.canvas.after(self.step_delay_rate, self.move)
        else:
            self.timer_end = time.time()
            print ("Time taken: " + str(self.timer_end-self.timer_start))
            print ("No of move calls: " + str(self.no_of_move_calls))
            for i in range(self.grid_ui_obj.grid_height/100+1):
                for j in range(self.grid_ui_obj.grid_width/100 + 1):
                    if self.grid_distribution[i][j] > 1:
                        print ("at pos " + str(i) + " " + str(j) + ": " + str(self.grid_distribution[i][j]))
            print ("Avg Dist away from center: " + str(self.avgDistFromCenter/self.no_of_move_calls))

    def get_best_possible_direction(self):
        dist_from_left_wall = self.get_distance_to_object(0, self.pos_y, self.pos_x, self.pos_y)
        dist_from_right_wall = self.get_distance_to_object(self.grid_ui_obj.grid_width, self.pos_y, self.pos_x, self.pos_y)
        dist_from_top_wall = self.get_distance_to_object(self.pos_x, 0, self.pos_x, self.pos_y)
        dist_from_bottom_wall = self.get_distance_to_object(self.pos_x, self.grid_ui_obj.grid_height, self.pos_x, self.pos_y)

        move_in_x = dist_from_right_wall - dist_from_left_wall
        move_in_y = dist_from_bottom_wall - dist_from_top_wall

        v1 = [move_in_x, move_in_y]
        v3 = [v1[0], v1[1]]

        for opponent in self.opponent_details:

            opponent_x = opponent.pos_x
            opponent_y = opponent.pos_y

            dir_from_ally = self.get_dir_away_from_object(opponent_x, opponent_y, self.pos_x, self.pos_y)
            dist_from_ally = self.get_distance_to_object(opponent_x, opponent_y, self.pos_x, self.pos_y)
            magnitude_in_opp_to_ally = self.grid_ui_obj.grid_diagonal/4 - dist_from_ally
            if magnitude_in_opp_to_ally > 0:
                dir_from_ally = math.radians(dir_from_ally)
                v2 = [magnitude_in_opp_to_ally * math.cos(dir_from_ally), magnitude_in_opp_to_ally * math.sin(dir_from_ally)]
                v3[0] += v2[0]
                v3[1] += v2[1]

        direction = math.degrees(math.atan2(v3[1], v3[0]))

        if direction < 0:
            return 360 + direction
        if direction >= 360:
            return direction-360
        return direction

    def is_collided(self, pos_x, pos_y, size, list_of_opponent):
        for opp in list_of_opponent:
            if abs(pos_x-opp.pos_x) <= opp.size and abs(pos_y-opp.pos_y) <= opp.size:
                self.stop = True




