"""
LED Blink

Description: Blinks an LED connected to GPIO 7.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Digital-IO#digital-output
"""

import time
from machine import Pin

# Define LED pin number
LED_PIN = 7

# Initialize pin: create Pin object and set to output mode (Pin.OUT)
led = Pin(LED_PIN, Pin.OUT)

while True:
    led.value(1)      # Turn on LED (1 represents high level)
    time.sleep(1)     # Wait for 1 second
    led.value(0)      # Turn off LED (0 represents low level)
    time.sleep(1)     # Wait for 1 second