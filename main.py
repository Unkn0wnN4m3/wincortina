from curtain import Curtain
from light_sensor import LightSensor
from machine import Pin
from phew import server
from rest import close, open
from wifi_connection import WiFiConnection

import config
import config_wifi

if __name__ == "__main__":
    try:
        cur = Curtain(config.SERVO_PIN)
        wifi = WiFiConnection(
            config_wifi.WIFI_CONFIG.get("ssid", ""),
            config_wifi.WIFI_CONFIG.get("password", ""),
        )

        if not wifi.connect():
            raise Exception("ssid or password is worng")

    except Exception as e:
        print(f"Initialization error: {e}")

    server.add_route("/open", open, methods=["GET"])
    server.add_route("/close", close, methods=["GET"])

    server.run()
