import socket
import msgpack
from spider_bot.model import settings
from spider_bot.model import enums
import msgpack_numpy as m
m.patch()


class Client:
    def __init__(self, host='127.0.0.1', port=settings.PORT):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_state(self):
        # 1. send cmd
        self.sock.sendto(
            msgpack.packb(
                [enums.CMD_GET_STATE, ],
                use_bin_type=True),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return msgpack.unpackb(data, raw=False)

    def set_action(self, action):
        # 1. send cmd
        self.sock.sendto(
            msgpack.packb(
                [enums.CMD_SET_ACTION, action],
                use_bin_type=True),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return msgpack.unpackb(data, raw=False)

    def enable_notify(self, enable):
        # 1. send cmd
        self.sock.sendto(
            msgpack.packb(
                [enums.CMD_ENABLE_NOTIFY, enable],
                use_bin_type=True),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return msgpack.unpackb(data, raw=False)

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    client = Client()
    print(client.enable_notify(1))
