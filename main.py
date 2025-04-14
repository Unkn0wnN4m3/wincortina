import uasyncio
from phew import server
from rest import close, open
from sensor_task import get_light_value
from wifi_connection import WiFiConnection

import config_wifi

if __name__ == "__main__":
    try:
        wifi = WiFiConnection(
            config_wifi.WIFI_CONFIG.get("ssid", ""),
            config_wifi.WIFI_CONFIG.get("password", ""),
        )

        if not wifi.connect():
            raise Exception("ssid or password is worng")

        server.add_route("/open", open, methods=["GET"])
        server.add_route("/close", close, methods=["GET"])

        uasyncio.create_task(get_light_value())  # Añade la tarea al loop

        server.run()
    except Exception as e:
        print(f"Initialization error: {e}")
