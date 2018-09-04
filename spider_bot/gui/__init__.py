from PyQt5 import QtWidgets
from spider_bot.gui import scene_view
from spider_bot.gui import scene


def main():
    import sys
    scene.Scene()
    app = QtWidgets.QApplication(sys.argv)
    view = scene_view.SceneView()
    view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
