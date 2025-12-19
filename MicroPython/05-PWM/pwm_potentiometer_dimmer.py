"""
PWM Potentiometer Dimmer

Description: Controls LED brightness using a potentiometer and PWM.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7
- Potentiometer -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/PWM
"""

import time
from machine import Pin, PWM, ADC

# 5000 Hz is smooth enough for LED dimming
FREQUENCY = 5000

# Define pins
LED_PIN = 7  # LED pin
POT_PIN = 8  # Potentiometer pin

# Create PWM object associated with GPIO 7
led_pwm = PWM(Pin(LED_PIN), freq=FREQUENCY, duty_u16=0)

# Initialize ADC (potentiometer)
pot = ADC(Pin(POT_PIN))

while True:
    # Read potentiometer analog value
    # read_u16() returns integer between 0 and 65535, scaled from raw value
    pot_value = pot.read_u16()

    # Set LED brightness
    # ADC read range (0-65535) matches PWM duty range (0-65535)
    # Can directly assign read value to PWM
    led_pwm.duty_u16(pot_value)

    time.sleep_ms(20)
