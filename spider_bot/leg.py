import math
from engine_3d import node
from engine_3d import vector


class Leg(node.Node):
    def __init__(
            self,
            shoulder_lenght=10,
            forearm_lenght=10,
            show_center=False,
            show_geometry=True,
            **kwargs):
        '''robot leg'''
        super(Leg, self).__init__(
            **kwargs)

        # 1. shoulder joints
        self.p_0 = node.Node(
            parent=self,
            pos=(0.0, 0.0, 0.0))

        self.p_1 = node.Node(
            parent=self.p_0,
            pos=(0.0, 0.0, 2))

        # 2. forearm joint
        self.p_2 = node.Node(
            parent=self.p_1,
            pos=(0.0, 0.0, shoulder_lenght))

        self.end = node.Node(
            parent=self.p_2,
            pos=(0.0, 0.0, forearm_lenght))

        if show_geometry:
            # import only for graphic mode
            from engine_3d import cylinder

            # create visibly parts
            self.cylinder_1 = cylinder.Cylinder(
                parent=self.p_0,
                length=5,
                show_center=show_center,
                axis=(0, 1, 0))

            self.cylinder_2 = cylinder.Cylinder(
                parent=self.p_1,
                length=4,
                show_center=show_center,
                offset=(-2, 0, 0))

            self.cylinder_3 = cylinder.Cylinder(
                parent=self.p_1,
                length=shoulder_lenght,
                show_center=show_center,
                axis=(0, 0, 1))

            self.cylinder_4 = cylinder.Cylinder(
                parent=self.p_2,
                length=4,
                show_center=show_center,
                offset=(-2, 0, 0))

            self.cylinder_5 = cylinder.Cylinder(
                parent=self.p_2,
                length=forearm_lenght,
                show_center=show_center,
                axis=(0, 0, 1))

    def move_end(self, pos):
        # 1. calk p_0 angle - vertical angle
        self.p_0.ang_y = self.get_proj_angle(
            self.o_z,
            self.o_x,
            self.world_to_frame(pos))

        # 2. calk triangle
        cur_pos = self.p_0.world_to_frame(pos) - self.p_1.pos
        len_a = self.p_2.pos.mag
        len_b = self.end.pos.mag
        len_c = cur_pos.mag

        # 2.1 p_1 angle
        tmp = (2 * len_a * len_c)
        if tmp != 0:
            tmp2 = (len_a * len_a + len_c * len_c - len_b * len_b)
            tmp3 = tmp2 / tmp
            try:
                angle = math.acos(tmp3)
            except ValueError:
                angle = 0.0
        else:
            angle = math.pi

        dir_angle = cur_pos.diff_angle(vector.Vector(0, 0, 1))

        # detect sign
        dir_angle = dir_angle if cur_pos.dot(
            vector.Vector(0., -1.0, 0.0)) > 0.0 else -dir_angle
        self.p_1.ang_x = dir_angle - angle

        # 2.2 p_2 angle
        try:
            angle = math.acos(
                (len_b * len_b + len_a * len_a - len_c * len_c) /
                (2 * len_a * len_b))
        except ValueError:
            angle = math.pi

        self.p_2.ang_x = math.pi - angle
