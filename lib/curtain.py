import gc
import time

from machine import ADC, PWM, Pin
import config
from micropython_servo_pdm_360 import ServoPDM360


class Curtain:
    def __init__(
        self, servo_pin: int, light_sersor_pin: int, magnetic_sensor_pin: int
    ) -> None:
        try:
            self.__init_hardware(servo_pin, light_sersor_pin, magnetic_sensor_pin)
            self.__init_status()
        except Exception as e:
            print(f"Initialization erro: {e}")
            raise

    def __init_hardware(
        self, servo_pin: int, light_sersor_pin: int, magnetic_sensor_pin: int
    ):
        self.servo_pwm = PWM(Pin(servo_pin))
        self.light_sensor = ADC(Pin(light_sersor_pin))
        self.magnetic_sensor = Pin(magnetic_sensor_pin, Pin.IN, Pin.PULL_UP)

        # create a servo object
        self.servo = ServoPDM360(
            pwm=self.servo_pwm,
            min_us=config.MIN_US,
            max_us=config.MAX_US,
            dead_zone_us=config.DEAD_ZONE_US,
            freq=config.FREQ,
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
        if self.__get_light_value_volts() > config.THRESHOLD:
            self.servo.turn_cv(config.FORCE)
        elif self.__get_light_value_volts() < config.THRESHOLD:
            self.servo.turn_ccv(config.FORCE)
        else:
            self.servo.stop()

    def __get_light_value_volts(self) -> float:
        input_value = self.light_sensor.read_u16()
        return config.VOUT * input_value / config.ADC_Q

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
