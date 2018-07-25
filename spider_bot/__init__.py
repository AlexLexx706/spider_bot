import time
import math
from PyQt5 import QtWidgets
from engine_3d import scene_view
from engine_3d import scene
from engine_3d import box
from engine_3d import cylinder
from engine_3d import shape
from engine_3d import sphere
from engine_3d import vector


class Leg(shape.Shape):
    def __init__(
            self,
            shoulder_lenght=10,
            forearm_lenght=10,
            **kwargs):
        '''robot leg'''
        super(Leg, self).__init__(
            show_center=True,
            **kwargs)
        # 1. shoulder joints
        self.p_0 = shape.Shape(
            parent=self,
            show_center=True)
        self.p_1 = shape.Shape(
            parent=self.p_0,
            show_center=True)

        # 2. forearm joint
        self.p_2 = shape.Shape(
            parent=self.p_1,
            show_center=True,
            pos=(0.0, 0.0, shoulder_lenght))

        self.end = shape.Shape(
            parent=self.p_2,
            show_center=True,
            pos=(0.0, 0.0, forearm_lenght))

        # self.p_0.ang_y = 0.1
        # self.p_1.ang_x = 0.1
        # self.p_2.ang_x = 0.1

    def move_end(self, pos):
        # 1. calk p_0 angle - vertical angle
        self.p_0.ang_y = self.get_proj_angle(
            self.o_z,
            self.o_x,
            self.world_to_frame(pos))

        # 2. calk tiangle
        cur_pos = self.p_0.world_to_frame(pos)
        len_a = self.p_2.pos.mag
        len_b = self.end.pos.mag
        len_c = cur_pos.mag

        # 2.1 p_1 angle
        angle = math.acos(
            (len_a * len_a + len_c * len_c - len_b * len_b) /
            (2 * len_a * len_c))
        self.p_1.ang_x = cur_pos.diff_angle(vector.Vector(0, 0, 1)) - angle

        # 2.2 p_2 angle
        self.p_2.ang_x = math.pi - math.acos(
            (len_b * len_b + len_a * len_a - len_c * len_c) /
            (2 * len_a * len_b))


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

        self.front_right_leg = Leg(
            parent=self,
            pos=(length / 2.0, 0.0, width / 2.0))

        self.point_center = (length / 2, 0, width / 2 + 15)
        self.test_point = sphere.Sphere(
            parent=self,
            pos=self.point_center)

    def update(self):
        super(SpiderBot, self).update()
        self.test_point.pos = (
            self.point_center[0] + math.sin(time.time()) * 4,
            self.point_center[1],
            self.point_center[2] + math.sin(time.time()) * 4)

        self.front_right_leg.move_end(
            self.test_point.frame_to_world((0, 0, 0)))


class MyScene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        self.camera.eye.pos[2] = 150
        self.camera.rotate_camera(1, -1)
        self.bot = SpiderBot()
        self.bot.pos = (10, 0, 0)


def main():
    import sys
    MyScene()
    app = QtWidgets.QApplication(sys.argv)
    view = scene_view.SceneView()
    view.show()
    sys.exit(app.exec_())
