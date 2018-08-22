import socket
import msgpack
import logging
import threading
import msgpack_numpy as m
from spider_bot.model import settings
from spider_bot.model import enums

m.patch()
LOG = logging.getLogger(__name__)


class Client:
    def __init__(self, host=settings.SERVER_IP, port=settings.SERVER_PORT):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.notify_thread = None
        self.notify_handler = None

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
            self.sock.sendto(
                msgpack.packb(
                    [enums.CMD_ADD_NOTIFY, port],
                    use_bin_type=True),
                self.server_address)
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return msgpack.unpackb(data, raw=False)
        else:
            LOG.warning('notifier already exist')

    def rm_notify(self):
        if self.notify_thread is not None:
            # 1. stop thread
            # self.notify_sock.shutdown(socket.SHUT_RDWR)
            self.notify_sock.shutdown(socket.SHUT_RD)
            self.notify_thread.join()
            self.notify_sock = None
            self.notify_thread = None

            # 2. send cmd
            self.sock.sendto(
                msgpack.packb(
                    [enums.CMD_RM_NOTIFY, self.notify_port],
                    use_bin_type=True),
                self.server_address)
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return msgpack.unpackb(data, raw=False)

    def listen_notify(self):
        """handler for listen notifys from server"""
        try:
            LOG.info('listen_notify begin')
            while 1:
                data, addr = self.notify_sock.recvfrom(
                    settings.MAX_PACKET_SIZE)
                # process notify
                if self.notify_handler:
                    error_code, data = msgpack.unpackb(data, raw=False)
                    self.notify_handler(error_code, data)
        except OSError:
            pass
        finally:
            LOG.info('listen_notify end')

    def close(self):
        # free socket and thread
        if self.notify_thread:
            self.rm_notify()
        self.sock.close()


if __name__ == "__main__":
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


