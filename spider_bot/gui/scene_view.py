from PyQt5 import QtCore
from engine_3d import scene_view
from spider_bot import enums


class SceneView(scene_view.SceneView):
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

    def closeEvent(self, event):
        event.accept()
        self.scene.client.close()
