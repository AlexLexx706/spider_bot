from engine_3d import scene
import spider_bot
from spider_bot.gui import client
import numpy as np

class Scene(scene.Scene):
    def __init__(self):
        scene.Scene.__init__(self)
        self.camera.eye.pos[2] = 150
        self.camera.rotate_camera(1, -1)
        self.bot = spider_bot.SpiderBot()
        self.bot.pos = (0, 0, 0)
        self.client = client.Client()
        self.client.notify_handler = self.notify_handler
        self.client.add_notify()

    def notify_handler(self, data):
        data.body_mat
        data.front_right_leg
        data.front_left_leg
        data.rear_right_leg
        data.rear_left_leg

        mat = np.array(data.body_mat)
        mat.shape = (4, 4)

        self.bot._matrix = mat
        self.bot.front_right_leg.move_end(list(data.front_right_leg.end))
        self.bot.front_left_leg.move_end(list(data.front_left_leg.end))
        self.bot.rear_right_leg.move_end(list(data.rear_right_leg.end))
        self.bot.rear_left_leg.move_end(list(data.rear_left_leg.end))
