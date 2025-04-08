import gc
import time

from machine import ADC, PWM, Pin
from micropython_servo_pdm_360 import ServoPDM360

import config


class Curtain:
    """Main class. All starts here"""

    def __init__(
        self, servo_pin: int, light_sensor_pin: int, magnetic_sensor_pin: int
    ) -> None:
        """
        Initializes the Curtain object.

        Args:
            servo_pin (int): The GPIO pin connected to the servo motor.
            light_sensor_pin (int): The GPIO pin connected to the light sensor.
            magnetic_sensor_pin (int): The GPIO pin connected to the magnetic sensor.
        """
        try:
            self.__init_hardware(servo_pin, light_sensor_pin, magnetic_sensor_pin)
            self.__init_status()
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def __init_hardware(
        self, servo_pin: int, light_sensor_pin: int, magnetic_sensor_pin: int
    ) -> None:
        """
        Initializes the hardware components of the Curtain system.

        Args:
            servo_pin (int): The GPIO pin connected to the servo motor.
            light_sensor_pin (int): The GPIO pin connected to the light sensor.
            magnetic_sensor_pin (int): The GPIO pin connected to the magnetic sensor.

        Sets up the PWM for servo control, ADC for light sensor reading, and
        input pin for the magnetic sensor.
        """
        self.servo_pwm = PWM(Pin(servo_pin))
        # WARN: ADC class may throw an error if the pin doesn't support analog
        # to digital function. Search for "pico w pinout"
        self.light_sensor = ADC(light_sensor_pin)  # Simplified ADC initialization
        self.magnetic_sensor = Pin(magnetic_sensor_pin, Pin.IN, Pin.PULL_UP)

        # create a servo object
        self.servo = ServoPDM360(
            pwm=self.servo_pwm,
            min_us=config.MIN_US,
            max_us=config.MAX_US,
            dead_zone_us=config.DEAD_ZONE_US,
            freq=config.FREQ,
        )

    def __init_status(self) -> None:
        """
        Initializes the status flags for the curtain system.

        Sets the initial state of the curtain as closed, not opening, and not running.
        These flags control the operational state of the curtain system.
        """
        self.is_open = False
        self.is_opening = False
        self.is_running = False

    def __handle_control_button(self) -> None:
        """
        Handles the magnetic sensor button press to toggle curtain movement.
        Uses debouncing to prevent false triggers.
        """
        current_state = self.magnetic_sensor.value()
        if current_state == 0:
            self.is_opening = not self.is_opening
            print(f"alarm status: {self.is_opening}")
            time.sleep(0.5)  # Debounce delay

    def __handle_curtain(
        self,
    ) -> None:
        """
        Controls the curtain movement based on light sensor readings.

        Compares the current light level against the configured threshold:
        - If light level is above threshold, turns the servo clockwise
        - If light level is below threshold, turns the servo counter-clockwise
        - If light level is at threshold, stops the servo

        This provides automated curtain control based on ambient light conditions.
        """
        if self.__get_light_value_volts() > config.THRESHOLD:
            self.servo.turn_cv(config.FORCE)
        elif self.__get_light_value_volts() < config.THRESHOLD:
            self.servo.turn_ccv(config.FORCE)
        else:
            self.servo.stop()

    def __get_light_value_volts(self) -> float:
        """
        Converts the raw ADC reading from the light sensor to a voltage value.

        Returns:
            float: The light sensor reading in volts, calculated by converting
                  the ADC's 16-bit value to the corresponding voltage based on
                  the reference voltage and ADC resolution.
        """
        input_value = self.light_sensor.read_u16()
        return config.VOUT * input_value / config.ADC_Q

    def start(self):
        """
        Starts the curtain control system and enters the main operation loop.

        This method initializes the system's running state and enters a continuous
        loop that monitors the control button and manages the curtain movement
        based on the current settings. The loop continues until an interruption
        occurs or the stop method is called.

        Exceptions are caught and handled, with appropriate cleanup performed
        via the stop method.
        """
        if not self.is_running:
            try:
                self.is_running = True
                print("Starting system...")
                while self.is_running:
                    self.__handle_control_button()

                    if self.is_opening:
                        self.__handle_curtain()
                    else:
                        self.servo.stop()
            except Exception as e:
                print(f"Main loop error: {e}")
                self.stop()

    def stop(self):
        """
        Stops the curtain control system and performs cleanup.

        This method resets all status flags (is_open, is_openning, is_running) to False,
        stops the servo motor to prevent further movement, and runs garbage collection
        to free up memory resources.

        Called when the system is intentionally stopped or when an error occurs that
        requires system shutdown.
        """
        print("system stoped")
        self.is_open = False
        self.is_opening = False
        self.is_running = False
        self.servo.stop()
        gc.collect()
