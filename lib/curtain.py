import time

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

            # create a servo object
            self.servo = ServoPDM360(
                pwm=self.servo_pwm,
                min_us=config.MIN_US,
                max_us=config.MAX_US,
                dead_zone_us=config.DEAD_ZONE_US,
                freq=config.FREQ,
            )
            # self.__init_status()
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def curtain_open(self) -> None:
        # start = time.ticks_ms()
        self.servo.turn_cv(config.FORCE)
        time.sleep(2)
        self.servo.stop()

        # if time.ticks_diff(time.ticks_ms(), start) > 2000:
        # self.servo.stop()

    def curtain_close(self) -> None:
        # start = time.ticks_ms()
        self.servo.turn_ccv(config.FORCE)
        time.sleep(1)
        self.servo.stop()

        # if time.ticks_diff(time.ticks_ms(), start) > 2000:
        #     self.servo.stop()
