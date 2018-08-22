import logging
import threading

LOG = logging.getLogger(__name__)

BOT = None
HANDLERS = {}


class NOTIFY:
    """static class use for help add/remove/itarate addess in notify list"""
    lock = threading.Lock()
    data = []
    notifier = None

    @classmethod
    def add(cls, addr):
        with cls.lock:
            if addr not in cls.data:
                cls.data.append(addr)
                if len(cls.data) == 1 and cls.notifier is not None:
                    cls.notifier.start()

    @classmethod
    def remove(cls, addr):
        with cls.lock:
            try:
                cls.data.remove(addr)
                if len(cls.data) == 0 and cls.notifier is not None:
                    cls.notifier.stop()
            except ValueError:
                LOG.warning('cannot remove addr:%s' % (addr, ))

    @classmethod
    def iterate(cls):
        with cls.lock:
            for addr in cls.data:
                yield addr

    @classmethod
    def register_notifier(cls, notifier):
        LOG.debug('register_notifier')
        cls.notifier = notifier

# init logging
logging.basicConfig(level=logging.DEBUG)
