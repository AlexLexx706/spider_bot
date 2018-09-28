from engine_3d import scene
import spider_bot
import spider_bot_client as client
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
        mat = np.array(data.body_mat)
        mat.shape = (4, 4)

        # ('shoulder_offset', ctypes.c_float),
        # ('shoulder_lenght', ctypes.c_float),
        # ('forearm_lenght', ctypes.c_float),

        self.bot._matrix = mat
        self.bot.front_right_leg.p_0.ang_y = data.front_right_leg.a_0
        self.bot.front_right_leg.p_1.ang_x = data.front_right_leg.a_1
        self.bot.front_right_leg.p_2.ang_x = data.front_right_leg.a_2
        self.bot.front_right_leg.pos = data.front_right_leg.geometry.pos

        pos = self.bot.front_right_leg.p_1.pos
        pos[2] = data.front_right_leg.geometry.shoulder_offset
        self.bot.front_right_leg.p_1.pos = pos
        pos = self.bot.front_right_leg.p_2.pos
        pos[2] = data.front_right_leg.geometry.shoulder_lenght
        self.bot.front_right_leg.p_2.pos = pos
        pos = self.bot.front_right_leg.end.pos
        pos[2] = data.front_right_leg.geometry.shoulder_lenght
        self.bot.front_right_leg.end.pos = pos

        self.bot.front_left_leg.p_0.ang_y = data.front_left_leg.a_0
        self.bot.front_left_leg.p_1.ang_x = data.front_left_leg.a_1
        self.bot.front_left_leg.p_2.ang_x = data.front_left_leg.a_2
        self.bot.front_left_leg.pos = data.front_left_leg.geometry.pos

        pos = self.bot.front_left_leg.p_1.pos
        pos[2] = data.front_left_leg.geometry.shoulder_offset
        self.bot.front_left_leg.p_1.pos = pos
        pos = self.bot.front_left_leg.p_2.pos
        pos[2] = data.front_left_leg.geometry.shoulder_lenght
        self.bot.front_left_leg.p_2.pos = pos
        pos = self.bot.front_left_leg.end.pos
        pos[2] = data.front_left_leg.geometry.shoulder_lenght
        self.bot.front_left_leg.end.pos = pos

        self.bot.rear_right_leg.p_0.ang_y = data.rear_right_leg.a_0
        self.bot.rear_right_leg.p_1.ang_x = data.rear_right_leg.a_1
        self.bot.rear_right_leg.p_2.ang_x = data.rear_right_leg.a_2
        self.bot.rear_right_leg.pos = data.rear_right_leg.geometry.pos

        pos = self.bot.rear_right_leg.p_1.pos
        pos[2] = data.rear_right_leg.geometry.shoulder_offset
        self.bot.rear_right_leg.p_1.pos = pos
        pos = self.bot.rear_right_leg.p_2.pos
        pos[2] = data.rear_right_leg.geometry.shoulder_lenght
        self.bot.rear_right_leg.p_2.pos = pos
        pos = self.bot.rear_right_leg.end.pos
        pos[2] = data.rear_right_leg.geometry.shoulder_lenght
        self.bot.rear_right_leg.end.pos = pos

        self.bot.rear_left_leg.p_0.ang_y = data.rear_left_leg.a_0
        self.bot.rear_left_leg.p_1.ang_x = data.rear_left_leg.a_1
        self.bot.rear_left_leg.p_2.ang_x = data.rear_left_leg.a_2
        self.bot.rear_left_leg.pos = data.rear_left_leg.geometry.pos

        pos = self.bot.rear_left_leg.p_1.pos
        pos[2] = data.rear_left_leg.geometry.shoulder_offset
        self.bot.rear_left_leg.p_1.pos = pos

        pos = self.bot.rear_left_leg.p_2.pos
        pos[2] = data.rear_left_leg.geometry.shoulder_lenght
        self.bot.rear_left_leg.p_2.pos = pos

        pos = self.bot.rear_left_leg.end.pos
        pos[2] = data.rear_left_leg.geometry.shoulder_lenght
        self.bot.rear_left_leg.end.pos = pos
