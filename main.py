from machine import PWM, Pin
from micropython_servo_pdm_360 import ServoPDM360
import time

# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(12))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# create a servo object
servo = ServoPDM360(
    pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq
)

if __name__ == "__main__":
    while True:
        servo.turn_cv(4)
        time.sleep(2)
        servo.turn_ccv(4)
        time.sleep(2)
