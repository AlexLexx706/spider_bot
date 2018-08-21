import time
import threading
import logging
from spider_bot.model import settings
from spider_bot.model import fake_scene
from spider_bot.model import common
from spider_bot.model import server
from spider_bot.model import handlers
import spider_bot

LOG = logging.getLogger(__name__)
LOG.debug('xxxx')
handlers.register()


def main():
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
            # make other actions
            else:
                time.sleep(sleep_period)
    except KeyboardInterrupt:
        LOG.debug("KeyboardInterrupt")
        server.close()
        server_thread.join()


if __name__ == "__main__":
    main()
