import time
from spider_bot import settings
from spider_bot import fake_scene
import spider_bot
import socket


def udp_server(host='127.0.0.1', port=1234):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        (data, addr) = s.recvfrom(128 * 1024)
        yield data


for data in udp_server():
    print("%r" % (data,))


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
            print(1)
        # make other actions
        else:
            time.sleep(sleep_period)


if __name__ == "__main__":
    main()
