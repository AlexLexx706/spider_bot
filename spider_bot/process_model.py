import time
from spider_bot import settings
from spider_bot import fake_scene
import spider_bot


def main():
    period = 1.0 / settings.UPDATES_PER_SECOND
    sleep_period = period / 10.0

    start_time = time.time()
    scene = fake_scene.FakeScene()
    spider_bot.SpiderBot(scene=scene)

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


if __name__ == "__main__":
    main()
