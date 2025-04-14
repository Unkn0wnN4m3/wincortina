# import time
import utime
from machine import PWM, Pin
from micropython_servo_pdm_360 import ServoPDM360RP2Async

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

            self.servo = ServoPDM360RP2Async(
                pwm=self.servo_pwm,
                min_us=config.MIN_US,
                max_us=config.MAX_US,
                dead_zone_us=config.DEAD_ZONE_US,
                freq=config.FREQ,
            )

            self.c_time_ms = config.TIME_PER_CM * config.CURTAINT_LENGT_CM
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def curtain_open(self) -> None:
        self.servo.turn_ccv_ms(force=config.FORCE, time_ms=self.c_time_ms)

    def curtain_close(self) -> None:
        self.servo.turn_cv_ms(force=config.FORCE, time_ms=self.c_time_ms)
