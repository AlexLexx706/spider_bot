import time
import math
from engine_3d import node
from spider_bot import leg
from spider_bot import enums
from engine_3d import vector
from engine_3d import transformations
import numpy as np


class SpiderBot(node.Node):
    '''
    Spider bot model
    '''
    # actions settings
    ROTATE_ANGLE = 20.0 / 180.0 * math.pi
    HALF_STEP_LEN = 6
    MOVE_TIME = 0.3
    STEP_HEIGHT = 4

    def __init__(
            self,
            length=10,
            width=10,
            height=3,
            show_center=False,
            show_geometry=True,
            **kwargs):
        super(SpiderBot, self).__init__(
            **kwargs)

        self.front_right_leg = leg.Leg(
            parent=self,
            show_center=show_center,
            show_geometry=show_geometry,
            pos=(length / 2.0, 0.0, width / 2.0))

        self.rear_right_leg = leg.Leg(
            parent=self,
            show_center=show_center,
            show_geometry=show_geometry,
            pos=(-length / 2.0, 0.0, width / 2.0))

        self.front_left_leg = leg.Leg(
            parent=self,
            axis=(-1, 0, 0),
            show_center=show_center,
            show_geometry=show_geometry,
            pos=(length / 2.0, 0.0, -width / 2.0))

        self.rear_left_leg = leg.Leg(
            parent=self,
            axis=(-1, 0, 0),
            show_center=show_center,
            show_geometry=show_geometry,
            pos=(-length / 2.0, 0.0, -width / 2.0))


        # use only in client part
        if show_geometry:
            from engine_3d import box
            self.box = box.Box(
                parent=self,
                length=length,
                width=width,
                height=height,
                offset=(0, height / 2, 0),
                show_center=show_center,
                show_geometry=show_geometry,
                color=(1, 0, 0, 1))

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
        self.action = enums.NOT_MOVE
        self.front_left_offset = vector.Vector(0, 0, 0)
        self.front_right_offset = vector.Vector(0, 0, 0)
        self.rear_left_offset = vector.Vector(0, 0, 0)
        self.rear_right_offset = vector.Vector(0, 0, 0)

        self.process_reset()

    def test_leg_move(self):
        pass

    def move_forward(self):
        self.action = enums.MOVE_FORWARD

    def move_backward(self):
        self.action = enums.MOVE_BACKWARD

    def rotate_left(self):
        self.action = enums.ROTATE_LEFT

    def rotate_right(self):
        self.action = enums.ROTATE_RIGHT

    def update(self):
        super(SpiderBot, self).update()

        # process control signals
        if self.move_state == -1 and self.rotate_state == -1:
            if self.action == enums.MOVE_FORWARD:
                self.move_state = 0
                self.begin_move = True
                self.half_step_len = self.HALF_STEP_LEN
            elif self.action == enums.MOVE_BACKWARD:
                self.move_state = 0
                self.begin_move = True
                self.half_step_len = -self.HALF_STEP_LEN
            elif self.action == enums.ROTATE_LEFT:
                self.rotate_state = 0
                self.begin_move = True
                self.turn_angle = self.ROTATE_ANGLE
            elif self.action == enums.ROTATE_RIGHT:
                self.rotate_state = 0
                self.begin_move = True
                self.turn_angle = -self.ROTATE_ANGLE

        # reset contrtol signal
        self.action = enums.NOT_MOVE

        self.process_move()
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

    @property
    def step_dt(self):
        if not self.begin_move:
            return (time.time() - self.start_time) / self.move_time, False

        self.start_time = time.time()
        self.begin_move = False
        return (time.time() - self.start_time) / self.move_time, True

    def process_rotate(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False
            self.first = True

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
            if self.first:
                self.first = False
                self.front_left_start = self.front_left_leg.end.g_pos
                self.dir = np.dot(
                    self.front_left_pos,
                    transformations.rotation_matrix(
                        self.turn_angle,
                        vector.Vector(0, 1, 0))[:3, :3].T) -\
                    self.front_left_start

            elif dt >= 1.0:
                dt = 1.0
                self.begin_move = True
                self.rotate_state = 1

            self.front_left_leg.move_end(
                self.front_left_start + self.dir * dt + up_vector)
        # move rear left leg
        elif self.rotate_state == 1:
            if self.first:
                self.first = False
                self.rear_left_start = self.rear_left_leg.end.g_pos
                self.dir = np.dot(
                    self.rear_left_pos,
                    transformations.rotation_matrix(
                        self.turn_angle,
                        vector.Vector(0, 1, 0))[:3, :3].T) -\
                    self.rear_left_start

            elif dt >= 1.0:
                dt = 1.0
                self.begin_move = True
                self.rotate_state = 2

            self.rear_left_leg.move_end(
                self.rear_left_start + self.dir * dt + up_vector)
        # rotate all points
        elif self.rotate_state == 2:
            if self.first:
                self.first = False
                self.front_left_start = self.front_left_leg.end.g_pos
                self.rear_left_start = self.rear_left_leg.end.g_pos
                self.front_right_start = self.front_right_leg.end.g_pos
                self.rear_right_start = self.rear_right_leg.end.g_pos

            elif dt >= 1.0:
                dt = 1.0
                self.begin_move = True
                self.rotate_state = 3

            mat = transformations.rotation_matrix(
                -self.turn_angle * dt,
                vector.Vector(0, 1, 0))[:3, :3].T

            self.front_left_leg.move_end(
                np.dot(self.front_left_start, mat))

            self.rear_left_leg.move_end(
                np.dot(self.rear_left_start, mat))

            self.front_right_leg.move_end(
                np.dot(self.front_right_start, mat))

            self.rear_right_leg.move_end(
                np.dot(self.rear_right_start, mat))

        # move rear right leg
        elif self.rotate_state == 3:
            if self.first:
                self.first = False
                self.rear_right_start = self.rear_right_leg.end.g_pos
                self.dir = np.dot(
                    self.rear_right_start,
                    transformations.rotation_matrix(
                        self.turn_angle,
                        vector.Vector(0, 1, 0))[:3, :3].T) -\
                    self.rear_right_start
            elif dt >= 1.0:
                dt = 1.0
                self.begin_move = True
                self.rotate_state = 4

            self.rear_right_leg.move_end(
                self.rear_right_start + self.dir * dt + up_vector)
        # move front right leg
        elif self.rotate_state == 4:
            if self.first:
                self.first = False
                self.front_right_start = self.front_right_leg.end.g_pos
                self.dir = np.dot(
                    self.front_right_start,
                    transformations.rotation_matrix(
                        self.turn_angle,
                        vector.Vector(0, 1, 0))[:3, :3].T) -\
                    self.front_right_start
            elif dt >= 1.0:
                dt = 1.0
                self.begin_move = True
                self.rotate_state = -1

            self.front_right_leg.move_end(
                self.front_right_start + self.dir * dt + up_vector)

    def process_move(self):
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

                self.cur_half_step_len = math.trunc((
                    self.start - self.front_right_leg.end.g_pos).mag /
                    math.fabs(self.half_step_len)) * self.half_step_len

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
