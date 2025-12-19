"""
Button Press Counter

Description: Counts and prints the number of button presses.

Wiring:
- ESP32-S3-Zero
- Button -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Digital-IO#digital-input
"""

import time
from machine import Pin

# Define pin
BUTTON_PIN = 8

# Initialize pin
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Initialize variables
last_button_state = 1  # Initial state defaults to 1 (high, not pressed)
count = 0

while True:
    # Read current button state
    current_button_state = button.value()

    # Check for edge transitions
    if last_button_state == 1 and current_button_state == 0:
        # Falling edge detected: button just pressed
        pass  # No action here

    elif last_button_state == 0 and current_button_state == 1:
        # Rising edge detected: button just released
        count += 1       # Increment counter
        print(count)     # Print current count

    # Update state for next iteration
    last_button_state = current_button_state