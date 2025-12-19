"""
Read Button State

Description: Reads and prints the state of a button connected to GPIO 8.

Wiring:
- ESP32-S3-Zero
- Button -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Digital-IO#digital-input
"""

import time
from machine import Pin

# Define button pin
BUTTON_PIN = 8

# Initialize pin as input with internal pull-up resistor
# When button is not pressed, pin reads as 1; when pressed (grounded), reads as 0
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

while True:
    # Read pin state
    button_state = button.value()

    # Print state to console
    print(button_state)

    # Add minimal delay to prevent excessive data refresh that could freeze console or block interrupts
    time.sleep_ms(20)