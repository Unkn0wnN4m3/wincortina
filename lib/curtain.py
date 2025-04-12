# import time
import utime
from machine import PWM, Pin
from micropython_servo_pdm_360 import ServoPDM360

import config


class Curtain:
    """Main class. All starts here"""

    def __init__(self, servo_pin: int) -> None:
        """
        Initializes the Curtain object.

        Args:
            servo_pin (int): The GPIO pin connected to the servo motor.
        """
        try:
            self.servo_pwm = PWM(Pin(servo_pin))

            self.servo = ServoPDM360(
                pwm=self.servo_pwm,
                min_us=config.MIN_US,
                max_us=config.MAX_US,
                dead_zone_us=config.DEAD_ZONE_US,
                freq=config.FREQ,
            )
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def curtain_open(self) -> None:
        self.servo.turn_cv(config.FORCE)
        utime.sleep_ms(config.SLEEPTIME * config.CURTAINT_LENGT_CM)
        self.servo.stop()

    def curtain_close(self) -> None:
        self.servo.turn_ccv(config.FORCE)
        utime.sleep_ms(config.SLEEPTIME * config.CURTAINT_LENGT_CM)
        self.servo.stop()
