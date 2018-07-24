import sys
from PyQt5 import QtWidgets
from engine_3d import scene_view
from engine_3d import scene
from engine_3d import box
from engine_3d import bone
from engine_3d import cylinder


class SpiderBot(box.Box):
    leg_width = 3
    leg_radius = 2
    leg_circle_1_lenght = 4

    def __init__(self, length=10, width=10, height=3):
        box.Box.__init__(self, length=length, width=width, height=height)
        self.center = bone.Bone(parent=self)
        self.leg_left_front_0 = cylinder.Cylinder(
            parent=self,
            radius=self.leg_radius,
            length=self.leg_circle_1_lenght,
            axis=(0, 1, 0),
            up=(-1, 0, 0),
            pos=(
                length / 2.0 - self.leg_width / 2.0,
                -self.leg_circle_1_lenght / 2.0,
                -width / 2.0))

        # self.leg_left_front_1 = box.Box(
        #     parent=self.leg_left_front_0,
        #     pos=(0, 0, 0),
        #     lenght=self.leg_width,
        #     height=self.leg_width,
        #     width=20)


class MyScene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        # add scene elements
        # self.box = box.Box(length=100, height=1, width=100, color=(1, 0, 0))
        # self.cylinder = cylinder.Cylinder(length=100, radius=10)
        self.camera.eye.pos[2] = 150
        self.camera.rotate_camera(1, -1)
        self.bot = SpiderBot()


def main():
    MyScene()
    app = QtWidgets.QApplication(sys.argv)
    view = scene_view.SceneView()
    view.show()
    sys.exit(app.exec_())
