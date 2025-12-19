"""
Button Control LED

Description: Turns an LED on when a button is pressed.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7
- Button -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Digital-IO#digital-io-exercise
"""

import time
from machine import Pin

# Define pin numbers
LED_PIN = 7
BUTTON_PIN = 8

# Initialize LED pin as output
led = Pin(LED_PIN, Pin.OUT)

# Initialize button pin as input with internal pull-up resistor
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

while True:
    # Read button state (0 = pressed, 1 = not pressed)
    button_state = button.value()

    if button_state == 0:
        # Button pressed, turn on LED
        led.value(1)
    else:
        # Button not pressed, turn off LED
        led.value(0)

    # Add minimal delay to reduce CPU usage
    time.sleep_ms(10)