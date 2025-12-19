"""
Button Toggle LED

Description: Toggles an LED on/off each time a button is pressed.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7
- Button -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Digital-IO#digital-io-exercise
"""

import time
from machine import Pin

# Define pins
LED_PIN = 7
BUTTON_PIN = 8

# Initialize pins
led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Initialize state variables
last_button_state = 1   # Previous button state, initialized as high (not pressed)
led_state = 0           # Current LED state: 0 = off, 1 = on

while True:
    # Read current button state
    current_button_state = button.value()

    # Detect rising edge: previous was low (pressed), current is high (released)
    if last_button_state == 0 and current_button_state == 1:
        # Toggle LED state (0 to 1, 1 to 0)
        led_state = not led_state

        # Apply new state to LED
        led.value(led_state)

        # Debounce delay
        time.sleep_ms(100)

    # Update state for next iteration
    last_button_state = current_button_state

    # Add minimal delay to reduce CPU usage
    time.sleep_ms(10)