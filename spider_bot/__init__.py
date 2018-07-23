import sys
from PyQt5 import QtWidgets
from engine_3d import scene_view


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = scene_view.SceneView()
    view.show()
    sys.exit(app.exec_())
