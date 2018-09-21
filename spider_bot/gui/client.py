import socket
import logging
import threading
import ctypes
from spider_bot import enums
from spider_bot.gui import settings
from spider_bot import settings as g_settings

LOG = logging.getLogger(__name__)


class Client:
    def __init__(self, host=settings.SERVER_IP, port=g_settings.SERVER_PORT):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.notify_thread = None
        self.notify_handler = None

    def get_state(self):
        # 1. send cmd
        self.sock.sendto(
            bytes(enums.Header(cmd=enums.CMD_GET_STATE, size=0)),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return enums.GetStateRes.from_buffer_copy(data)

    def set_action(self, action):
        # 1. send cmd
        cmd = enums.SetActionCmd()
        cmd.header.cmd = enums.CMD_SET_ACTION
        cmd.header.size = ctypes.sizeof(enums.SetActionCmd) -\
            ctypes.sizeof(enums.Header)
        cmd.action = action

        self.sock.sendto(
            bytes(cmd),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return enums.ResHeader.from_buffer_copy(data)

    def add_notify(self, port=settings.CLIENT_NOTIFY_PORT):
        if self.notify_thread is None:
            LOG.info('add_notify port:%s' % (port, ))
            # 1. create socket for listen
            self.notify_port = port
            self.notify_sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.notify_sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.notify_sock.bind(('0.0.0.0', port))

            # 2. create listen notify thread
            self.notify_thread = threading.Thread(target=self.listen_notify)
            self.notify_thread.start()

            # 3. send cmd
            cmd = enums.AddNotifyCmd()
            cmd.header.cmd = enums.CMD_ADD_NOTIFY
            cmd.header.size = ctypes.sizeof(enums.AddNotifyCmd) -\
                ctypes.sizeof(enums.Header)
            cmd.port = port
            print("add_notify port:", cmd.port)
            self.sock.sendto(
                bytes(cmd),
                self.server_address)
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return enums.ResHeader.from_buffer_copy(data)
        else:
            LOG.warning('notifier already exist')

    def rm_notify(self):
        if self.notify_thread is not None:
            print('rm_notify port:%s' % (self.notify_port, ))
            # 1. stop thread
            # self.notify_sock.shutdown(socket.SHUT_RDWR)
            self.notify_sock.shutdown(socket.SHUT_RD)
            self.notify_thread.join()
            self.notify_sock = None
            self.notify_thread = None

            # 2. send cmd
            cmd = enums.RmNotifyCmd()
            cmd.header.cmd = enums.CMD_RM_NOTIFY
            cmd.header.size = ctypes.sizeof(enums.RmNotifyCmd) -\
                ctypes.sizeof(enums.Header)
            cmd.port = self.notify_port
            self.sock.sendto(
                bytes(cmd),
                self.server_address)
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return enums.ResHeader.from_buffer_copy(data)

    def manage_servo(self, cmd, address, limmit):
        # 1. send cmd
        # print(cmd, address, limmit)
        packet = enums.ManageServoCmd()
        packet.header.cmd = enums.CMD_RM_NOTIFY
        packet.header.size = ctypes.sizeof(packet) -\
            ctypes.sizeof(enums.Header)
        packet.cmd = cmd
        packet.address = address
        packet.limmit = limmit

        self.sock.sendto(
            bytes(packet),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return enums.ManageServoRes.from_buffer_copy(data)

    def listen_notify(self):
        """handler for listen notifys from server"""
        try:
            LOG.info('listen_notify begin')
            while 1:
                data, addr = self.notify_sock.recvfrom(
                    g_settings.MAX_PACKET_SIZE)
                # process notify
                if self.notify_handler:
                    self.notify_handler(
                        enums.GetStateRes.from_buffer_copy(data))
        except OSError:
            pass
        finally:
            LOG.info('listen_notify end')

    def close(self):
        # free socket and thread
        if self.notify_thread:
            self.rm_notify()
        self.sock.close()

    def set_leg_geometry(self, leg_num, leg_geometry):
        cmd = enums.SetLegGeometry()
        cmd.header.cmd = enums.CMD_SET_LEG_GEOMETRY
        cmd.header.size = ctypes.sizeof(enums.SetLegGeometry) -\
            ctypes.sizeof(enums.Header)
        cmd.leg_num = leg_num
        cmd.geometry = leg_geometry

        self.sock.sendto(
            bytes(cmd),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return enums.ResHeader.from_buffer_copy(data)


def test_servo_calibrate():
    import math
    client = Client()

    calibrations_data = [
        {'address': 0, "min": -45, 'max': 45, "name": "front right leg 0"},
        {'address': 1, "min": -90, 'max': 90, "name": "front right leg 1"},
        {'address': 2, "min": 0, 'max': 100, "name": "front right leg 2"},
        {'address': 3, "min": -45, 'max': 45, "name": "rear right leg 0"},
        {'address': 4, "min": -90, 'max': 90, "name": "rear right leg 1"},
        {'address': 5, "min": 0, 'max': 100, "name": "rear right leg 2"},
        {'address': 6, "min": -45, 'max': 45, "name": "front left leg 0"},
        {'address': 7, "min": -90, 'max': 90, "name": "front left leg 1"},
        {'address': 8, "min": 0, 'max': 100, "name": "front left leg 2"},
        {'address': 9, "min": -45, 'max': 45, "name": "rear left leg 0"},
        {'address': 10, "min": -90, 'max': 90, "name": "rear left leg 1"},
        {'address': 11, "min": 0, 'max': 100, "name": "rear left leg 2"},
    ]
    # 1. get model state
    print("start calibration servos:")
    input('reset addresses:')
    print("res:%s\n" % (
        client.manage_servo(
            enums.ManageServoCmd.ResetAddressesCmd, 0, 0).error_desc, ))

    for calib_data in calibrations_data:
        addr = calib_data['address']
        input('set address:%s, %s:' % (addr, calib_data['name']))
        print("res:%s\n" % (
            client.manage_servo(
                enums.ManageServoCmd.SetAddressCmd, addr, 0).error_desc, ))

        input('start EnableReadAngles, %s:' % (calib_data['name'], ))
        res = client.manage_servo(
            enums.ManageServoCmd.EnableReadAngles,
            addr,
            0).error_desc
        print("res:%s\n" % (res, ))

        angle = calib_data['min']
        input('calibrate min, turn servo to angle:%s, %s:' % (
            angle, calib_data['name']))
        res = client.manage_servo(
            enums.ManageServoCmd.SetMinLimmitCmd,
            addr,
            angle / 180. * math.pi)
        print("res:%s\n" % (res.error_desc, ))

        if res.error != 0:
            return

        angle = calib_data['max']
        input('calibrate max, turn servo to angle:%s, %s:' % (
            angle, calib_data['name']))
        res = client.manage_servo(
            enums.ManageServoCmd.SetMaxLimmitCmd,
            addr,
            angle / 180.0 * math.pi)
        print("res:%s\n" % (res.error_desc, ))

        if res.error != 0:
            return

        # test servo calibration:
        print('test servo calibration, %s:' % (calib_data['name'], ))

        angle = calib_data['min']
        input('move servo %d to:%s angle, %s' % (
            addr, angle, calib_data['name']))
        res = client.manage_servo(
            enums.ManageServoCmd.MoveServo,
            addr,
            angle / 180.0 * math.pi).error_desc

        print("res:%s\n" % (res, ))

        angle = calib_data['max']
        input('move servo %s to:%s angle, %s' % (
            addr, angle, calib_data['name']))
        res = client.manage_servo(
            enums.ManageServoCmd.MoveServo,
            addr,
            angle / 180.0 * math.pi).error_desc

        print("res:%s\n" % (res, ))

    input('enable read angles:')
    print(" res:%s" % (
        client.manage_servo(
            enums.ManageServoCmd.EnableReadAngles,
            addr,
            0).error_desc, ))

    input('unload servo')
    res = client.manage_servo(
        enums.ManageServoCmd.UnloadServosCmd,
        addr,
        angle).error_desc

    print("res:%s" % (res, ))


def test_servo_enable_sterring():
    client = Client()
    input('unload servo')

    addr = 2
    res = client.manage_servo(
        enums.ManageServoCmd.UnloadServosCmd,
        addr,
        0).error
    print("res:%s" % (res, ))

    input('enable sterring:')
    print("res:%s" % (
        client.manage_servo(
            enums.ManageServoCmd.EnableSteringCmd,
            addr,
            0).error, ))


def test_servo_read_angles():
    client = Client()
    addr = 0
    input('unload servo')

    addr = 2
    res = client.manage_servo(
        enums.ManageServoCmd.UnloadServosCmd,
        addr,
        0).error
    print("res:%s" % (res, ))

    input('start EnableReadAngles:')
    print("res:%s" % (client.manage_servo(
        enums.ManageServoCmd.EnableReadAngles,
        enums.ManageServoCmd.BroadcastAddr,
        0).error, ))


def test_set_leg_geometry():
    client = Client()
    input('get bot state:')
    res = client.get_state()
    print("res:%s" % (res.header.error, ))

    if (res.header.error != enums.NO_ERROR):
        return
    geometry = res.front_right_leg.geometry
    print(
        "geometry: pos:%s shoulder_offset:%s "
        "shoulder_lenght:%s forearm_lenght:%s" % (
            [v for v in geometry.pos],
            geometry.shoulder_offset,
            geometry.shoulder_lenght,
            geometry.forearm_lenght))
    # length in santimetrs
    shoulder_offset = 8
    shoulder_lenght = 8
    forearm_lenght = 4

    legs_geometry = [
        enums.LegGeometry(
            (enums.ctypes.c_float * 3)(10, -2, 5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght),
        enums.LegGeometry(
            (enums.ctypes.c_float * 3)(-10, -2, 5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght),
        enums.LegGeometry(
            (enums.ctypes.c_float * 3)(10, -2, -5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght),
        enums.LegGeometry(
            (enums.ctypes.c_float * 3)(-10, -2, -5),
            shoulder_offset,
            shoulder_lenght,
            forearm_lenght)
    ]
    input('set legs geometry:')
    for leg_num, leg_geometry in enumerate(legs_geometry):
        print("set_leg geometry leg_num:%s res:%s" % (
            leg_num,
            client.set_leg_geometry(leg_num, leg_geometry).error))


if __name__ == "__main__":
    # test_set_leg_geometry()
    # exit(0)
    # test_servo_read_angles()
    # exit(0)
    test_servo_calibrate()
    #test_servo_enable_sterring()
    exit(0)

    def notify_handler(code, data):
        pass
        # print('code:%s data:%s' % (code, data))

    client = Client()
    client.notify_handler = notify_handler
    client.add_notify()
    import time
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()


