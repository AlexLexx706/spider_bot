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
    show_center = True

    def __init__(
            self,
            shoulder_lenght=10,
            forearm_lenght=10,
            **kwargs):
        '''robot leg'''
        super(Leg, self).__init__(
            show_center=self.show_center,
            **kwargs)

        # 1. shoulder joints
        self.p_0 = shape.Shape(
            parent=self,
            show_center=self.show_center)

        self.p_1 = shape.Shape(
            parent=self.p_0,
            show_center=self.show_center)

        # 2. forearm joint
        self.p_2 = shape.Shape(
            parent=self.p_1,
            show_center=self.show_center,
            pos=(0.0, 0.0, shoulder_lenght))

        self.end = shape.Shape(
            parent=self.p_2,
            show_center=self.show_center,
            pos=(0.0, 0.0, forearm_lenght))

        # create visibly parts
        self.cylinder_1 = cylinder.Cylinder(
            parent=self.p_0,
            length=5,
            axis=(0, 1, 0))

        self.cylinder_2 = cylinder.Cylinder(
            parent=self.p_1,
            length=4,
            offset=(-2, 0, 0))

        self.cylinder_3 = cylinder.Cylinder(
            parent=self.p_1,
            length=shoulder_lenght,
            axis=(0, 0, 1))

        self.cylinder_4 = cylinder.Cylinder(
            parent=self.p_2,
            length=4,
            offset=(-2, 0, 0))

        self.cylinder_5 = cylinder.Cylinder(
            parent=self.p_2,
            length=forearm_lenght,
            axis=(0, 0, 1))


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
        tmp = (2 * len_a * len_c)
        if tmp != 0:
            tmp2 = (len_a * len_a + len_c * len_c - len_b * len_b)
            tmp3 = tmp2 / tmp
            print(tmp, tmp2, tmp3)
            try:
                angle = math.acos(tmp3)
            except ValueError:
                angle = 0
        else:
            angle = 0

        self.p_1.ang_x = cur_pos.diff_angle(vector.Vector(0, 0, 1)) - angle

        # 2.2 p_2 angle
        try:
            angle = math.acos(
                (len_b * len_b + len_a * len_a - len_c * len_c) /
                (2 * len_a * len_b))
        except ValueError:
            angle = math.pi

        self.p_2.ang_x = math.pi - angle

        # print('control angles: %s, %s, %s' % (
        #     self.p_0.ang_y, self.p_1.ang_x, self.p_2.ang_x))


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

        self.front_left_leg = Leg(
            parent=self,
            axis=(-1, 0, 0),
            pos=(length / 2.0, 0.0, -width / 2.0))

        self.rear_left_leg = Leg(
            parent=self,
            pos=(-length / 2.0, 0.0, width / 2.0))

        self.rear_right_leg = Leg(
            parent=self,
            axis=(-1, 0, 0),
            pos=(-length / 2.0, 0.0, -width / 2.0))

        self.point_center_1 = (length / 2, 0, width / 2 + 15)
        self.test_point_1 = sphere.Sphere(
            parent=self,
            pos=self.point_center_1)

        self.point_center_2 = (length / 2, 0, -(width / 2 + 15))
        self.test_point_2 = sphere.Sphere(
            parent=self,
            pos=self.point_center_2)

        self.point_center_3 = (-length / 2, 0, width / 2 + 15)
        self.test_point_3 = sphere.Sphere(
            parent=self,
            pos=self.point_center_3)

        self.point_center_4 = (-length / 2, 0, -(width / 2 + 15))
        self.test_point_4 = sphere.Sphere(
            parent=self,
            pos=self.point_center_4)

    def update(self):
        super(SpiderBot, self).update()
        self.test_point_1.pos = (
            self.point_center_1[0] + math.sin(time.time()) * 20,
            self.point_center_1[1],
            self.point_center_1[2] + math.sin(time.time()) * 4)

        self.front_right_leg.move_end(
            self.test_point_1.frame_to_world((0, 0, 0)))

        self.test_point_2.pos = (
            self.point_center_2[0] + math.sin(time.time()) * 4,
            self.point_center_2[1],
            self.point_center_2[2] - math.sin(time.time()) * 4)

        self.front_left_leg.move_end(
            self.test_point_2.frame_to_world((0, 0, 0)))

        self.test_point_3.pos = (
            self.point_center_3[0] + math.sin(time.time()) * 4,
            self.point_center_3[1],
            self.point_center_3[2] - math.sin(time.time()) * 4)

        self.rear_left_leg.move_end(
            self.test_point_3.frame_to_world((0, 0, 0)))

        self.test_point_4.pos = (
            self.point_center_4[0] + math.sin(time.time()) * 4,
            self.point_center_4[1],
            self.point_center_4[2] - math.sin(time.time()) * 4)

        self.rear_right_leg.move_end(
            self.test_point_4.frame_to_world((0, 0, 0)))


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
