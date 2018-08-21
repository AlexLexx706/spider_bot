import socket
import msgpack
from spider_bot.model import settings
from spider_bot.model import enums

# Create a UDP socket
server_address = ('127.0.0.1', settings.PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    # 1. send cmd
    sock.sendto(
        msgpack.packb(
            [20, ],
            use_bin_type=True),
        server_address)

    # 2. recv data
    data, server = sock.recvfrom(4096)
    print('receive data:%s' % (msgpack.unpackb(data, raw=False), ))

finally:
    sock.close()
