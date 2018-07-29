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
    # actions
    NOT_MOVE = 0
    MOVE_FORWARD = 1
    MOVE_BACKWARD = 2
    ROTATE_LEFT = 3
    ROTATE_RIGHT = 4

    # actions settings
    ROTATE_ANGLE = 20.0 / 180.0 * math.pi
    HALF_STEP_LEN = 6
    MOVE_TIME = 0.2
    STEP_HEIGHT = 4

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

        self.move_state = -1
        self.begin_move = True
        self.move_time = self.MOVE_TIME
        self.half_step_len = self.HALF_STEP_LEN
        self.step_height = self.STEP_HEIGHT

        self.rotate_state = -1
        self.turn_angle = self.ROTATE_ANGLE

        # not move at start
        self.action = self.NOT_MOVE
        self.front_left_offset = vector.Vector(0, 0, 0)
        self.front_right_offset = vector.Vector(0, 0, 0)
        self.rear_left_offset = vector.Vector(0, 0, 0)
        self.rear_right_offset = vector.Vector(0, 0, 0)
        self.process_reset()

    def move_forward(self):
        self.action = self.MOVE_FORWARD

    def move_backward(self):
        self.action = self.MOVE_BACKWARD

    def rotate_left(self):
        self.action = self.ROTATE_LEFT

    def rotate_right(self):
        self.action = self.ROTATE_RIGHT

    def update(self):
        super(SpiderBot, self).update()

        # process control signals
        if self.move_state == -1 and self.rotate_state == -1:
            if self.action == self.MOVE_FORWARD:
                self.move_state = 0
                self.begin_move = True
                self.half_step_len = self.HALF_STEP_LEN
            elif self.action == self.MOVE_BACKWARD:
                self.move_state = 0
                self.begin_move = True
                self.half_step_len = -self.HALF_STEP_LEN
            elif self.action == self.ROTATE_LEFT:
                self.rotate_state = 0
                self.begin_move = True
                self.turn_angle = self.ROTATE_ANGLE
            elif self.action == self.ROTATE_RIGHT:
                self.rotate_state = 0
                self.begin_move = True
                self.turn_angle = -self.ROTATE_ANGLE

        # reset contrtol signal
        self.action = self.NOT_MOVE

        self.process_move_2()
        self.process_rotate()

    def process_reset(self):
        self.front_left_leg.move_end(
            self.front_left_pos)

        self.front_right_leg.move_end(
            self.front_right_pos)

        self.rear_left_leg.move_end(
            self.rear_left_pos)

        self.rear_right_leg.move_end(
            self.rear_right_pos)

    def process_move(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False

            # init pose
            if self.move_state == 0:
                self.process_reset()
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

    def process_rotate(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False

            # init state
            if self.rotate_state == 0:
                self.process_reset()

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

    def process_move_2(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False
            self.first = True

            # init pose
            # if self.move_state == 0:
            #     self.process_reset()
        dt = (time.time() - self.start_time) / self.move_time

        # 1. move front_left forward
        if self.move_state == 0:
            # begin move leg
            if self.first:
                self.first = False
                self.start_pos = self.front_left_leg.end.g_pos
                self.dir = (
                    self.front_left_pos +
                    vector.Vector(self.half_step_len, 0, 0)) - self.start_pos
            # end step
            elif dt >= 1.0:
                self.begin_move = True
                self.move_state = 1
                self.first = True
                dt = 1.0
            # move leg
            self.front_left_leg.move_end(
                self.start_pos +
                self.dir * dt +
                vector.Vector(0, self.step_height * math.sin(math.pi * dt), 0))
        # 2. 4 points
        elif self.move_state == 1:
            if self.first:
                self.first = False
                self.start_front_left = self.front_left_leg.end.g_pos
                self.start_front_right = self.front_right_leg.end.g_pos
                self.start_rear_left = self.rear_left_leg.end.g_pos
                self.start_rear_right = self.rear_right_leg.end.g_pos
            elif dt >= 1.0:
                self.begin_move = True
                self.move_state = 2
                self.first = True
                dt = 1.0
            # move legs
            direction = -vector.Vector(self.half_step_len, 0, 0) * dt

            self.front_left_leg.move_end(self.start_front_left + direction)
            self.front_right_leg.move_end(self.start_front_right + direction)
            self.rear_left_leg.move_end(self.start_rear_left + direction)
            self.rear_right_leg.move_end(self.start_rear_right + direction)

        # 4. move right rear leg
        elif self.move_state == 2:
            if self.first:
                self.first = False
                self.start = self.rear_right_leg.end.g_pos

                self.cur_half_step_len = math.trunc((self.start - self.front_right_leg.end.g_pos).mag / self.half_step_len) * self.half_step_len
                print('self.half_step_len:%s self.cur_half_step_len:%s' % (self.half_step_len, self.cur_half_step_len, ))

            elif dt >= 1.0:
                self.begin_move = True
                self.move_state = 3
                self.first = True
                dt = 1.0
            # move leg
            self.rear_right_leg.move_end(
                self.start +
                vector.Vector(
                    self.cur_half_step_len * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))
        # 3. move right front leg
        elif self.move_state == 3:
            if self.first:
                self.first = False
                self.start = self.front_right_leg.end.g_pos
            # end
            elif dt >= 1.0:
                self.begin_move = True
                self.move_state = 4
                self.first = True
                dt = 1.0

            # move leg
            self.front_right_leg.move_end(
                self.start +
                vector.Vector(
                    self.half_step_len * 2 * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))
        # 4. 4 points
        elif self.move_state == 4:
            if self.first:
                self.first = False
                self.start_front_left = self.front_left_leg.end.g_pos
                self.start_front_right = self.front_right_leg.end.g_pos
                self.start_rear_left = self.rear_left_leg.end.g_pos
                self.start_rear_right = self.rear_right_leg.end.g_pos
            # end
            elif dt >= 1.0:
                self.begin_move = True
                self.move_state = 5
                self.first = True
                dt = 1.0

            # move legs
            direction = vector.Vector(-self.half_step_len, 0, 0) * dt

            self.front_left_leg.move_end(self.start_front_left + direction)
            self.rear_left_leg.move_end(self.start_rear_left + direction)
            self.front_right_leg.move_end(self.start_front_right + direction)
            self.rear_right_leg.move_end(self.start_rear_right + direction)
        # 5. move rear left
        elif self.move_state == 5:
            if self.first:
                self.first = False
                self.start = self.rear_left_leg.end.g_pos
            # end
            elif dt >= 1.0:
                self.begin_move = True
                self.move_state = -1
                dt = 1.0

            # move leg
            self.rear_left_leg.move_end(
                self.start +
                vector.Vector(
                    self.half_step_len * 2 * dt,
                    self.step_height * math.sin(math.pi * dt),
                    0))
