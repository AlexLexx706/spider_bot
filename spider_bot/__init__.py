import time
import math
from PyQt5 import QtWidgets
from engine_3d import scene_view
from engine_3d import scene
from engine_3d import box
from engine_3d import bone
from engine_3d import cylinder
from engine_3d import shape


class SpiderBot(box.Box):
    '''
    Spider bot model
    '''
    leg_width = 3
    cylinder_radius = 1
    cylinder_lenght = 4
    shoulder_lenght = 10
    forearm_lenght = 10

    def __init__(self, length=10, width=10, height=3):
        box.Box.__init__(
            self,
            length=length,
            width=width,
            height=height,
            offset=(0, height / 2, 0),
            show_center=True)

        # 1. left_front_leg
        self.leg_left_front_0 = cylinder.Cylinder(
            parent=self,
            axis=(0, 1, 0),
            radius=self.cylinder_radius,
            length=self.cylinder_lenght,
            pos=(length / 2, 0, -width / 2))

        # self.leg_left_front_0.visible = False

        self.leg_left_front_1 = cylinder.Cylinder(
            parent=self.leg_left_front_0,
            axis=(0, -1, 0),
            up=(-1, 0, 0),
            radius=self.cylinder_radius,
            length=self.cylinder_lenght,
            offset=(-self.cylinder_lenght / 2, 0, 0))

        self.leg_left_front_shoulder = cylinder.Cylinder(
            parent=self.leg_left_front_1,
            axis=(0, 0, 1),
            radius=self.cylinder_radius,
            length=self.shoulder_lenght)

        self.leg_left_front_2 = cylinder.Cylinder(
            parent=self.leg_left_front_1,
            radius=self.cylinder_radius,
            length=self.cylinder_lenght,
            offset=(-self.cylinder_lenght / 2, 0, 0),
            pos=(0, 0, self.shoulder_lenght))

        self.leg_left_front_forearms = cylinder.Cylinder(
            parent=self.leg_left_front_2,
            axis=(0, 0, 1),
            radius=self.cylinder_radius,
            length=self.shoulder_lenght)

        self.leg_left_front_end = shape.Shape(
            parent=self.leg_left_front_2,
            pos=(0, 0, self.forearm_lenght),
            show_center=True)

        self.leg_left_front_end.center_length = 2

        self.leg_left_front_0.rotate(-0.4, (0, 1, 0))
        self.leg_left_front_1.rotate(0.5, (0, 1, 0))
        self.leg_left_front_2.rotate(-0.5, (1, 0, 0))

    def update(self):
        box.Box.update(self)
        self.leg_left_front_0.rotate(math.sin(time.time()) * 0.01, (0, 1, 0))
        self.leg_left_front_1.rotate(math.sin(time.time() * 4) * 0.01, (0, 1, 0))
        self.leg_left_front_2.rotate(math.sin(time.time() * 4) * 0.01, (1, 0, 0))



class MyScene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        # add scene elements
        # self.box = box.Box(length=100, height=1, width=100, color=(1, 0, 0))
        # self.cylinder = cylinder.Cylinder(length=100, radius=10)
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
