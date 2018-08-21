import time
import threading
import logging
from spider_bot.model import settings
from spider_bot.model import fake_scene
from spider_bot.model import common
from spider_bot.model import server
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
    scene = fake_scene.FakeScene()
    common.BOT = spider_bot.SpiderBot(scene=scene)

    # create and start udp server
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

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
        LOG.debug("KeyboardInterrupt")
        server.close()
        server_thread.join()


if __name__ == "__main__":
    main()
