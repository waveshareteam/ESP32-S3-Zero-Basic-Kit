"""
PWM Breathing LED

Description: Creates a breathing LED effect using PWM.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/PWM
"""

import time
from machine import Pin, PWM

# 5000 Hz is smooth enough for LED dimming
FREQUENCY = 5000

# Define LED pin (GPIO 7)
LED_PIN = 7

# Create PWM object
led_pwm = PWM(Pin(LED_PIN),freq=FREQUENCY,duty_u16=0)

while True:
    # Gradually increase brightness (fade in)
    for duty in range(0, 65536, 1000):
        led_pwm.duty_u16(duty)  # Apply current duty cycle
        time.sleep_ms(10)       # Brief delay to control breathing speed

    # Gradually decrease brightness (fade out)
    for duty in range(65535, -1, -1000):
        led_pwm.duty_u16(duty)  # Apply current duty cycle
        time.sleep_ms(10)       # Brief delay to control breathing speed