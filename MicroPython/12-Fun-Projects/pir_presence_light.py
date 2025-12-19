"""
Pir Presence Light

Description: Uses a PIR sensor to detect motion and controls a WS2812 LED strip, turning it on when presence is detected.

Wiring:
- ESP32-S3-Zero
- PIR VCC -> 5V
- PIR GND -> GND
- PIR -> GPIO 7
- WS2812 VCC -> 5V
- WS2812 GND -> GND
- WS2812 DI -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-3-Presence-Light
"""

import time
import machine
import neopixel

# --- Configuration ---
PIR_PIN = 7
LED_PIN = 8
NUM_LEDS = 8
TIMEOUT = 5000  # How long the light stays on after person leaves (milliseconds)
COLOR = (128, 0, 128)

# --- Initialization ---
pir = machine.Pin(PIR_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

def switch_light(on):
    color = COLOR if on else (0, 0, 0)
    np.fill(color)
    np.write()

# --- Main program ---
try:
    print("System started... (Press Ctrl+C to stop)")
    is_on = False
    last_motion_time = time.ticks_ms()

    # Force lights off at start to prevent state mismatch
    switch_light(False)

    while True:
        current_time = time.ticks_ms()

        # --- Core logic ---

        # 1. Keep updating timestamp as long as sensor is high (presence detected)
        if pir.value() == 1:
            last_motion_time = current_time
            # Turn on light if not already on
            if not is_on:
                print("Presence detected -> Turn on light")
                switch_light(True)
                is_on = True

        # 2. When sensor is low (no presence), start timeout calculation
        else:
            # Only check timeout when light is on
            if is_on:
                # Calculate: current time - last presence time
                duration = time.ticks_diff(current_time, last_motion_time)

                if duration > TIMEOUT:
                    print("Timeout without presence -> Turn off light")
                    switch_light(False)
                    is_on = False
                    # Small delay to prevent false triggers from voltage fluctuations
                    time.sleep_ms(1000)

        # Check frequency: 100ms is sufficient for fast response and low power consumption
        time.sleep_ms(100)

except KeyboardInterrupt:
    print("\nManually stopped by user")

finally:
    # Ensure lights are off in any case
    print("Cleaning up resources, turning off LED strip...")
    switch_light(False)