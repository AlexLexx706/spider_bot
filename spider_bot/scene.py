from PyQt5 import QtWidgets, QtCore
from engine_3d import scene_view
from engine_3d import scene
import spider_bot
from spider_bot.model import client
from spider_bot.model import enums


class MyScene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        self.camera.eye.pos[2] = 150
        self.camera.rotate_camera(1, -1)
        self.bot = spider_bot.SpiderBot()
        self.bot.pos = (0, 0, 0)
        self.client = client.Client()
        self.client.notify_handler = self.notify_handler
        self.client.add_notify()

    def notify_handler(self, res, data):
        mat = data['mat']
        self.bot._matrix = mat[0]

        self.bot.front_right_leg._matrix =     mat[1][0]
        self.bot.front_right_leg.p_0._matrix = mat[1][1]
        self.bot.front_right_leg.p_1._matrix = mat[1][2]
        self.bot.front_right_leg.p_2._matrix = mat[1][3]
        self.bot.front_right_leg.end._matrix = mat[1][3]

        self.bot.front_left_leg._matrix =     mat[2][0]
        self.bot.front_left_leg.p_0._matrix = mat[2][1]
        self.bot.front_left_leg.p_1._matrix = mat[2][2]
        self.bot.front_left_leg.p_2._matrix = mat[2][3]
        self.bot.front_left_leg.end._matrix = mat[2][3]

        self.bot.rear_right_leg._matrix =     mat[3][0]
        self.bot.rear_right_leg.p_0._matrix = mat[3][1]
        self.bot.rear_right_leg.p_1._matrix = mat[3][2]
        self.bot.rear_right_leg.p_2._matrix = mat[3][3]
        self.bot.rear_right_leg.end._matrix = mat[3][3]

        self.bot.rear_left_leg._matrix =     mat[4][0]
        self.bot.rear_left_leg.p_0._matrix = mat[4][1]
        self.bot.rear_left_leg.p_1._matrix = mat[4][2]
        self.bot.rear_left_leg.p_2._matrix = mat[4][3]
        self.bot.rear_left_leg.end._matrix = mat[4][3]




class MySceneView(scene_view.SceneView):
    def __init__(self, *args, **kwargs):
        scene_view.SceneView.__init__(self, *args, **kwargs)

    def keyPressEvent(self, event):
        scene_view.SceneView.keyPressEvent(self, event)

        if event.key() == QtCore.Qt.Key_Left:
            self.scene.client.set_action(enums.ROTATE_LEFT)
        elif event.key() == QtCore.Qt.Key_Right:
            self.scene.client.set_action(enums.ROTATE_RIGHT)
        elif event.key() == QtCore.Qt.Key_Up:
            self.scene.client.set_action(enums.MOVE_FORWARD)
        elif event.key() == QtCore.Qt.Key_Down:
            self.scene.client.set_action(enums.MOVE_BACKWARD)

        # if event.key() == QtCore.Qt.Key_Left:
        #     self.scene.bot.rotate_left()
        # elif event.key() == QtCore.Qt.Key_Right:
        #     self.scene.bot.rotate_right()
        # elif event.key() == QtCore.Qt.Key_Up:
        #     self.scene.bot.move_forward()
        # elif event.key() == QtCore.Qt.Key_Down:
        #     self.scene.bot.move_backward()


def main():
    import sys
    MyScene()
    app = QtWidgets.QApplication(sys.argv)
    view = MySceneView()
    view.show()
    sys.exit(app.exec_())
