import time
import math
from engine_3d import box
from engine_3d import sphere
from spider_bot import leg
from engine_3d import vector
from engine_3d import transformations
import numpy as np


class SpiderBot(box.Box):
    '''
    Spider bot model
    '''
    leg_width = 3
    cylinder_radius = 1
    cylinder_lenght = 4
    shoulder_lenght = 10
    forearm_lenght = 10

    def __init__(self, length=10, width=10, height=3, **kwargs):
        print('length:%s' % (length, ))
        super(SpiderBot, self).__init__(
            length=length,
            width=width,
            height=height,
            offset=(0, height / 2, 0),
            show_center=True,
            color=(1, 0, 0, 1),
            **kwargs)

        self.front_right_leg = leg.Leg(
            parent=self,
            pos=(length / 2.0, 0.0, width / 2.0))

        self.front_left_leg = leg.Leg(
            parent=self,
            axis=(-1, 0, 0),
            pos=(length / 2.0, 0.0, -width / 2.0))

        self.rear_left_leg = leg.Leg(
            parent=self,
            pos=(-length / 2.0, 0.0, -width / 2.0))

        self.rear_right_leg = leg.Leg(
            parent=self,
            axis=(-1, 0, 0),
            pos=(-length / 2.0, 0.0, width / 2.0))

        # leg end point
        self.front_right_pos = (length / 2, -4, width / 2 + 8)
        self.front_left_pos = (length / 2, -4, -(width / 2 + 8))
        self.rear_right_pos = (-length / 2, -4, width / 2 + 8)
        self.rear_left_pos = (-length / 2, -4, -(width / 2 + 8))

        self.move_state = 0
        self.begin_move = True
        self.move_time = 0.4
        self.half_step_len = 8
        self.step_height = 3

        self.rotate_state = 0
        self.turn_angle = 20.0 / 180.0 * math.pi

    def update(self):
        super(SpiderBot, self).update()
        # self.move_forward()
        # if self.move_state == -1:
        #     self.move_state = 0
        self.rotate_step()
        if self.rotate_state == -1:
            self.rotate_state = 0


    def move_forward(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False

            # init pose
            if self.move_state == 0:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos)

                self.rear_left_leg.move_end(
                    self.rear_left_pos)

                self.rear_right_leg.move_end(
                    self.rear_right_pos)
        dt = (time.time() - self.start_time) / self.move_time

        # 1. move front_left forward
        if self.move_state == 0:
            # end
            if dt >= 1.0:
                self.begin_move = True
                self.move_state = 1
                dt = 1.0

            self.front_left_leg.move_end(
                self.front_left_pos + vector.Vector(
                    self.half_step_len * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))
        # 2. 3 points
        elif self.move_state == 1:
            if dt >= 1.0:
                self.begin_move = True
                self.move_state = 2
                dt = 1.0
            # move legs
            direction = vector.Vector(self.half_step_len, 0, 0) * dt
            self.front_left_leg.move_end(
                self.front_left_pos + vector.Vector(
                    self.half_step_len, 0, 0) - direction)
            self.front_right_leg.move_end(self.front_right_pos - direction)
            self.rear_left_leg.move_end(self.rear_left_pos - direction)
            self.rear_right_leg.move_end(self.rear_right_pos - direction)

        # 3. move right rear leg
        elif self.move_state == 2:
            if dt >= 1.0:
                self.begin_move = True
                self.move_state = 3
                dt = 1.0

            # move leg
            self.rear_right_leg.move_end(
                self.rear_right_pos -
                vector.Vector(self.half_step_len, 0, 0) +
                vector.Vector(
                    self.half_step_len * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))
        # 3. move right front leg
        elif self.move_state == 3:
            # end
            if dt >= 1.0:
                self.begin_move = True
                self.move_state = 4
                dt = 1.0

            # move leg
            self.front_right_leg.move_end(
                self.front_right_pos -
                vector.Vector(self.half_step_len, 0, 0) +
                vector.Vector(
                    self.half_step_len * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))
        # 3. move right front leg
        elif self.move_state == 4:
            if dt >= 1.0:
                self.begin_move = True
                self.move_state = -1
                dt = 1.0
            # move leg
            self.rear_left_leg.move_end(
                self.rear_left_pos -
                vector.Vector(self.half_step_len, 0, 0) +
                vector.Vector(
                    self.half_step_len * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))

    def rotate_step(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False

            # init state
            if self.rotate_state == 0:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos)

                self.rear_left_leg.move_end(
                    self.rear_left_pos)

                self.rear_right_leg.move_end(
                    self.rear_right_pos)

        dt = (time.time() - self.start_time) / self.move_time
        up_vector = vector.Vector(
            0,
            self.step_height * math.sin(math.pi * dt),
            0)

        # move front left leg
        if self.rotate_state == 0:
            if dt < 1.0:
                angle = dt * self.turn_angle
            else:
                angle = self.turn_angle
                self.begin_move = True
                self.rotate_state = 1
            self.front_left_leg.move_end(
                up_vector + np.dot(
                    self.front_left_pos,
                    transformations.rotation_matrix(
                        angle,
                        vector.Vector(0, 1, 0))[:3, :3].T))
        # move rear left leg
        elif self.rotate_state == 1:
            if dt < 1.0:
                angle = dt * self.turn_angle
            else:
                angle = self.turn_angle
                self.begin_move = True
                self.rotate_state = 2

            self.rear_left_leg.move_end(
                up_vector + np.dot(
                    self.rear_left_pos,
                    transformations.rotation_matrix(
                        angle,
                        vector.Vector(0, 1, 0))[:3, :3].T))
        # rotate all points
        elif self.rotate_state == 2:
            if dt < 1.0:
                angle_1 = (1.0 - dt) * self.turn_angle
                angle_2 = dt * -self.turn_angle
            else:
                angle_1 = 0
                angle_2 = -self.turn_angle
                self.begin_move = True
                self.rotate_state = 3

            mat_1 = transformations.rotation_matrix(
                angle_1,
                vector.Vector(0, 1, 0))[:3, :3].T

            mat_2 = transformations.rotation_matrix(
                angle_2,
                vector.Vector(0, 1, 0))[:3, :3].T

            self.front_left_leg.move_end(
                np.dot(self.front_left_pos, mat_1))

            self.rear_left_leg.move_end(
                np.dot(self.rear_left_pos, mat_1))

            self.front_right_leg.move_end(
                np.dot(self.front_right_pos, mat_2))

            self.rear_right_leg.move_end(
                np.dot(self.rear_right_pos, mat_2))

        # move rear right leg
        elif self.rotate_state == 3:
            if dt < 1.0:
                angle = (1.0 - dt) * -self.turn_angle
            else:
                angle = 0
                self.begin_move = True
                self.rotate_state = 4

            self.rear_right_leg.move_end(
                up_vector + np.dot(
                    self.rear_right_pos,
                    transformations.rotation_matrix(
                        angle,
                        vector.Vector(0, 1, 0))[:3, :3].T))
        # move front right leg
        elif self.rotate_state == 4:
            if dt < 1.0:
                angle = (1.0 - dt) * -self.turn_angle
            else:
                angle = 0
                self.begin_move = True
                self.rotate_state = -1

            self.front_right_leg.move_end(
                up_vector + np.dot(
                    self.front_right_pos,
                    transformations.rotation_matrix(
                        angle,
                        vector.Vector(0, 1, 0))[:3, :3].T))

