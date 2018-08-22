import socket
import msgpack
import logging
import traceback
import threading

from spider_bot.model import settings
from spider_bot.model import enums
from spider_bot.model import common


LOG = logging.getLogger(__name__)


class Server:
    """simple UDP server, for reveive data from clients"""

    def __init__(self, host=settings.HOST, port=settings.SERVER_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((settings.HOST, settings.SERVER_PORT))
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        try:
            while 1:
                data, addr = self.sock.recvfrom(settings.MAX_PACKET_SIZE)
                msg = msgpack.unpackb(data, raw=False)

                # try execute command
                try:
                    res = common.HANDLERS[msg[0]](
                        None if len(msg) == 1 else msg[1], addr=addr)
                except KeyError as e:
                    err_desc = 'wrong command:%s' % (e,)
                    LOG.warning(err_desc)
                    res = (enums.WRONG_COMMAND, err_desc)
                except Exception:
                    LOG.warning(traceback.format_exc())
                    res = (enums.UNKNOWN_ERROR, traceback.format_exc())

                self.sock.sendto(
                    msgpack.packb(res, use_bin_type=True),
                    addr)
        except OSError as e:
            LOG.warning(e)

    def close(self):
        """stop server"""
        if self.thread:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.thread.join()
            self.sock = None
            self.thread = None
