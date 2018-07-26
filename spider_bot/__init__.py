import time
import math
from engine_3d import box
from engine_3d import sphere
from spider_bot import leg
from engine_3d import vector


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

    def update(self):
        super(SpiderBot, self).update()
        self.move_forward()

    def move_forward(self):
        if self.begin_move:
            self.start_time = time.time()
            self.begin_move = False
        dt = (time.time() - self.start_time) / self.move_time

        # 1. move front_left forward
        if self.move_state == 0:
            # move by line
            if dt < 1.0:
                self.front_left_leg.move_end(
                    self.front_left_pos +
                    vector.Vector(
                        self.half_step_len * dt,
                        self.step_height * math.sin(math.pi * dt), 0))
                self.front_right_leg.move_end(self.front_right_pos)
                self.rear_left_leg.move_end(self.rear_left_pos)
                self.rear_right_leg.move_end(self.rear_right_pos)
            # end move
            else:
                self.front_left_leg.move_end(
                    self.front_left_pos +
                    vector.Vector(self.half_step_len, 0, 0))
                self.front_right_leg.move_end(self.front_right_pos)
                self.rear_left_leg.move_end(self.rear_left_pos)
                self.rear_right_leg.move_end(self.rear_right_pos)

                self.begin_move = True
                self.move_state = 1
        # 2. 3 points
        elif self.move_state == 1:
            if dt < 1.0:
                self.front_left_leg.move_end(
                    self.front_left_pos +
                    vector.Vector(self.half_step_len, 0, 0) +
                    vector.Vector(-self.half_step_len, 0, 0) * dt)

                self.front_right_leg.move_end(
                    self.front_right_pos -
                    vector.Vector(self.half_step_len, 0, 0) * dt)

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0) * dt)

                self.rear_right_leg.move_end(
                    self.rear_right_pos -
                    vector.Vector(self.half_step_len, 0, 0) * dt)

            # end move
            else:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_right_leg.move_end(
                    self.rear_right_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.begin_move = True
                self.move_state = 2
        # 3. move right rear leg
        elif self.move_state == 2:
            if dt < 1.0:
                self.front_left_leg.move_end(self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_right_leg.move_end(
                    self.rear_right_pos -
                    vector.Vector(self.half_step_len, 0, 0) +
                    vector.Vector(
                        self.half_step_len * dt,
                        self.step_height * math.sin(math.pi * dt),
                        0))
            # end move
            else:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_right_leg.move_end(
                    self.rear_right_pos)

                self.begin_move = True
                self.move_state = 3

        # 3. move right front leg
        elif self.move_state == 3:
            if dt < 1.0:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos -
                    vector.Vector(self.half_step_len, 0, 0) +
                    vector.Vector(
                        self.half_step_len * dt,
                        self.step_height * math.sin(math.pi * dt),
                        0))

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_right_leg.move_end(
                    self.rear_right_pos)

            # end move
            else:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos)

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0))

                self.rear_right_leg.move_end(
                    self.rear_right_pos)

                self.begin_move = True
                self.move_state = 4

        # 3. move right front leg
        elif self.move_state == 4:
            if dt < 1.0:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos)

                self.rear_left_leg.move_end(
                    self.rear_left_pos -
                    vector.Vector(self.half_step_len, 0, 0) +
                    vector.Vector(
                        self.half_step_len * dt,
                        self.step_height * math.sin(math.pi * dt),
                        0))
                self.rear_right_leg.move_end(
                    self.rear_right_pos)
            # end move
            else:
                self.front_left_leg.move_end(
                    self.front_left_pos)

                self.front_right_leg.move_end(
                    self.front_right_pos)

                self.rear_left_leg.move_end(
                    self.rear_left_pos)

                self.rear_right_leg.move_end(
                    self.rear_right_pos)

                self.begin_move = True
                self.move_state = 0

        def rotate(self):
            if self.begin_move:
                self.start_time = time.time()
                self.begin_move = False
            dt = (time.time() - self.start_time) / self.move_time

            # move front left leg
            if self.rotate_state == 0:
                pass
            # move rear left leg
            elif self.rotate_state == 1:
                pass
            # rotate all points
            elif self.rotate_state == 2:
                pass
            # move rear right leg
            elif self.rotate_state == 3:
                pass
            # move front right leg
            elif self.rotate_state == 4:
                pass

