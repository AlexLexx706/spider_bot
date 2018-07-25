import time
import math
from PyQt5 import QtWidgets
from engine_3d import scene_view
from engine_3d import scene
from engine_3d import box
from engine_3d import sphere
from spider_bot import leg


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
            pos=(-length / 2.0, 0.0, width / 2.0))

        self.rear_right_leg = leg.Leg(
            parent=self,
            axis=(-1, 0, 0),
            pos=(-length / 2.0, 0.0, -width / 2.0))

        self.point_center_1 = (length / 2, 0, width / 2 + 8)
        self.test_point_1 = sphere.Sphere(
            # parent=self,
            pos=self.point_center_1,
            show_center=True)

        self.point_center_2 = (length / 2, 0, -(width / 2 + 8))
        self.test_point_2 = sphere.Sphere(
            # parent=self,
            pos=self.point_center_2,
            show_center=True)

        self.point_center_3 = (-length / 2, 0, width / 2 + 8)
        self.test_point_3 = sphere.Sphere(
            # parent=self,
            pos=self.point_center_3,
            show_center=True)

        self.point_center_4 = (-length / 2, 0, -(width / 2 + 8))
        self.test_point_4 = sphere.Sphere(
            # parent=self,
            pos=self.point_center_4,
            show_center=True)

    def update(self):
        super(SpiderBot, self).update()
        # self.test_point_1.pos = (
        #     self.point_center_1[0],
        #     self.point_center_1[1] + math.sin(time.time()) * 20,
        #     self.point_center_1[2])

        # self.test_point_2.pos = (
        #     self.point_center_2[0],
        #     self.point_center_2[1] + math.sin(time.time()) * 20,
        #     self.point_center_2[2])

        # self.test_point_3.pos = (
        #     self.point_center_3[0],
        #     self.point_center_3[1] + math.sin(time.time()) * 20,
        #     self.point_center_3[2])

        # self.test_point_4.pos = (
        #     self.point_center_4[0],
        #     self.point_center_4[1] + math.sin(time.time()) * 20,
        #     self.point_center_4[2])

        self.pos = (
            math.cos(time.time()) * 4,
            math.sin(time.time()) * 2 + 6,
            math.cos(time.time() * 4) * 4)

        self.ang_x = math.cos(time.time() * 20) * 0.2
        self.ang_y = math.cos(time.time() * 4) * 0.3

        self.front_right_leg.move_end(
            self.test_point_1.frame_to_world((0, 0, 0)))

        self.front_left_leg.move_end(
            self.test_point_2.frame_to_world((0, 0, 0)))

        self.rear_left_leg.move_end(
            self.test_point_3.frame_to_world((0, 0, 0)))

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
