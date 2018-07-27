from PyQt5 import QtWidgets, QtCore
from engine_3d import scene_view
from engine_3d import scene
import spider_bot


class MyScene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        self.camera.eye.pos[2] = 150
        self.camera.rotate_camera(1, -1)
        self.bot = spider_bot.SpiderBot()
        self.bot.pos = (0, 0, 0)


class MySceneView(scene_view.SceneView):
    def __init__(self, *args, **kwargs):
        scene_view.SceneView.__init__(self, *args, **kwargs)

    def keyPressEvent(self, event):
        scene_view.SceneView.keyPressEvent(self, event)

        if event.key() == QtCore.Qt.Key_Left:
            self.scene.bot.rotate_left()
        elif event.key() == QtCore.Qt.Key_Right:
            self.scene.bot.rotate_right()
        elif event.key() == QtCore.Qt.Key_Up:
            self.scene.bot.move_forward()
        elif event.key() == QtCore.Qt.Key_Down:
            self.scene.bot.move_backward()


def main():
    import sys
    MyScene()
    app = QtWidgets.QApplication(sys.argv)
    view = MySceneView()
    view.show()
    sys.exit(app.exec_())
