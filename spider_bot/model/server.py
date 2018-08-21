import socket
import msgpack
import logging
import traceback
from spider_bot.model import settings
from spider_bot.model import common
from spider_bot.model import enums

LOG = logging.getLogger(__name__)


def run():
    """simple UDP server, for reveive data from clients"""
    try:
        LOG.debug('start run')
        common.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        common.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        LOG.debug("Listening on udp %s:%s" % (
            settings.HOST, settings.PORT))
        common.SOCK.bind((settings.HOST, settings.PORT))

        while True:
            data, addr = common.SOCK.recvfrom(128 * 1024)
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
                res = (enums.UNKNOWN_ERROR, traceback.format_exc())

            common.SOCK.sendto(
                msgpack.packb(res, use_bin_type=True),
                addr)
    except OSError as e:
        LOG.warning(e)
    finally:
        LOG.debug("run complete")


def close():
    """stop server"""
    if common.SOCK is not None:
        common.SOCK.shutdown(socket.SHUT_RDWR)
        common.SOCK.close()
        common.SOCK = None
