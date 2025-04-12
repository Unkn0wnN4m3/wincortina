from curtain import Curtain
from phew import server

import config

cur = Curtain(config.SERVO_PIN)


def open(request):
    print(request)
    cur.curtain_open()
    return "", 200


def close(request):
    print(request)
    cur.curtain_close()
    return "", 200
