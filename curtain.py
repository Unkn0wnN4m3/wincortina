import gc
import time

from machine import ADC, PWM, Pin
from micropython_servo_pdm_360 import ServoPDM360


class Curtain:
    def __init__(
        self, servo_pin: int, light_sersor_pin: int, magnetic_sensor_pin: int
    ) -> None:
        self.servo_pwm = PWM(Pin(servo_pin))
        self.light_sensor = ADC(Pin(light_sersor_pin))
        self.magnetic_sensor = Pin(magnetic_sensor_pin, Pin.IN, Pin.PULL_UP)

        try:
            self.__init_hardware()
            self.__init_status()
        except Exception as e:
            print(f"Initialization erro: {e}")
            raise

    def __init_hardware(self):
        # Set the parameters of the servo pulses, more details in the "Documentation" section
        freq = 50
        min_us = 400
        max_us = 2550
        dead_zone_us = 150

        # create a servo object
        self.servo = ServoPDM360(
            pwm=self.servo_pwm,
            min_us=min_us,
            max_us=max_us,
            dead_zone_us=dead_zone_us,
            freq=freq,
        )

    def __init_status(self):
        self.is_open = False
        self.is_openning = False
        self.is_running = False

    def __handle_control_button(self):
        current_state = self.magnetic_sensor.value()
        if current_state == 0:
            self.is_openning = not self.is_openning
            print(f"alarm status: {self.is_openning}")
            time.sleep(0.5)

    def __handle_curtain(
        self,
    ):
        if self.__get_light_value_volts() > 1.0:
            self.servo.turn_cv(4)
        elif self.__get_light_value_volts() < 1.0:
            self.servo.turn_ccv(4)
        else:
            self.servo.stop()

    def __get_light_value_volts(self):
        ADC_Q = 2**16
        VOUT = 3.3
        INPUT_VALUE = self.light_sensor.read_u16()
        return VOUT * INPUT_VALUE / ADC_Q

    def start(self):
        if not self.is_running:
            try:
                self.is_running = True
                print("Starting system...")
                while self.is_running:
                    self.__handle_control_button()

                    if self.is_openning:
                        self.__handle_curtain()
                    else:
                        self.servo.stop()
            except Exception as e:
                print(f"Main loop error: {e}")
                self.stop()

    def stop(self):
        print("system stoped")
        self.is_open = False
        self.is_openning = False
        self.is_running = False
        self.servo.stop()
        gc.collect()
