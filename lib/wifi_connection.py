import time

import network


class WiFiConnection:
    def __init__(self, ssid: str, password: str):
        """Initialize WiFi connection with SSID and password"""
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.is_connected = False

    def connect(self, timeout: int = 10) -> bool:
        """
        Connect to WiFi network
        Args:
            timeout: Maximum time to wait for connection in seconds
        Returns:
            bool: True if connected successfully, False otherwise
        """
        print(f"Connecting to WiFi network: {self.ssid}...")

        if not self.wlan.active():
            self.wlan.active(True)

        # Already connected
        if self.wlan.isconnected():
            print("Already connected")
            self.is_connected = True
            return True

        self.wlan.connect(self.ssid, self.password)

        # Wait for connection with timeout
        start_time = time.time()
        while not self.wlan.isconnected():
            if time.time() - start_time > timeout:
                print("Connection timeout")
                self.is_connected = False
                return False
            time.sleep(0.1)

        # Successfully connected
        print("Connected successfully")
        print(f"IP Address: {self.wlan.ifconfig()[0]}")
        self.is_connected = True
        return True

    def disconnect(self):
        """Disconnect from WiFi network"""
        if self.wlan.active():
            self.wlan.disconnect()
            self.wlan.active(False)
            self.is_connected = False
            print("Disconnected from WiFi")

    def check_connection(self) -> bool:
        """
        Check if currently connected to WiFi
        Returns:
            bool: True if connected, False otherwise
        """
        self.is_connected = self.wlan.isconnected()
        return self.is_connected

    def get_ip(self) -> str:
        """
        Get current IP address
        Returns:
            str: Current IP address or empty string if not connected
        """
        if self.check_connection():
            return self.wlan.ifconfig()[0]
        return ""
