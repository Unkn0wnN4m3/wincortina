from machine import ADC, Pin

import config


class LightSensor:
    def __init__(self, light_sensor_pin: int) -> None:
        try:
            self.light_sensor = ADC(Pin(light_sensor_pin))
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def get_value(self) -> float:
        input_value = self.light_sensor.read_u16()
        return config.VOUT * input_value / config.ADC_Q
