from curtain import Curtain
from phew import server

import config

cur = Curtain(config.SERVO_PIN)


def open(request):
    print(request)
    cur.curtain_open()
    return server.Response(
        '{"status": "opened"}', 200, {"Content-Type": "application/json"}
    )


def close(request):
    print(request)
    cur.curtain_close()
    return server.Response(
        '{"status": "closed"}', 200, {"Content-Type": "application/json"}
    )
