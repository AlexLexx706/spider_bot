import time
import logging
from spider_bot.model import settings
from spider_bot.model import common
from spider_bot.model import server as server_mod
from spider_bot.model import handlers
from spider_bot.model import notifier

import spider_bot

LOG = logging.getLogger(__name__)


class FakeScene:
    """used for calculate ik in bot"""
    def __init__(self):
        self.frames = []

    def update(self):
        for frame in self.frames:
            frame.update()


def main():
    # register server handlers
    handlers.register()

    # registry notifier class, use for send clients notifys
    common.NOTIFY.register_notifier(notifier.Notifier)

    period = 1.0 / settings.UPDATES_PER_SECOND
    sleep_period = period / 10.0

    start_time = time.time()
    scene = FakeScene()
    common.BOT = spider_bot.SpiderBot(scene=scene)

    # create and start udp server
    server = server_mod.Server()

    # controler
    try:
        while 1:
            cur_time = time.time()
            dt = cur_time - start_time

            # update model
            if dt >= period:
                start_time = cur_time
                scene.update()

                # send notify for all clients
                notifier.Notifier.process()
            # make other actions
            else:
                time.sleep(sleep_period)
    except KeyboardInterrupt:
        LOG.debug('KeyboardInterrupt')
    finally:
        server.close()


if __name__ == "__main__":
    main()
