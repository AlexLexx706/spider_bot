import msgpack
import threading
import logging
import socket
from spider_bot.model import common
from spider_bot.model import handlers

LOG = logging.getLogger(__name__)


class Notifier:
    """used for send notifis to clients"""
    lock = threading.Lock()
    sock = None

    @classmethod
    def start(cls):
        with cls.lock:
            if cls.sock is None:
                # use socket for send notify
                cls.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @classmethod
    def stop(cls):
        with cls.lock:
            if cls.sock is not None:
                cls.sock.close()
                cls.sock = None

    @classmethod
    def process(cls):
        with cls.lock:
            if cls.sock:
                for addr in common.NOTIFY.iterate():
                    data = msgpack.packb(
                        handlers.get_state(None),
                        use_bin_type=True)
                    cls.sock.sendto(data, addr)
