"""
Potentiometer LED Strip

Description: Reads potentiometer value via ADC to control WS2812 LED strip color transitions.

Wiring:
- ESP32-S3-Zero
- Potentiometer VCC -> 3.3V
- Potentiometer GND -> GND
- Potentiometer -> GPIO 7
- WS2812 VCC -> 5V
- WS2812 GND -> GND
- WS2812 DI-> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-4-LED-Strip
"""

import time
from machine import Pin, ADC
import neopixel

# --- Configuration parameters ---
POT_PIN_NUM = 7   # Potentiometer pin
NEO_PIN_NUM = 8   # WS2812 pin
NUM_LEDS = 8      # Number of LEDs

# --- Color definitions (R, G, B) ---
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN  = (0, 255, 0)
COLOR_RED    = (255, 0, 0)
COLOR_OFF    = (0, 0, 0)

# Initialize WS2812 LED strip
np = neopixel.NeoPixel(Pin(NEO_PIN_NUM), NUM_LEDS)

# Initialize potentiometer (ADC)
pot = ADC(Pin(POT_PIN_NUM))

def update_leds(adc_val):
    """
    Update LED states based on ADC value
    adc_val: 0 - 65535
    """
    # Map 0-65535 to 0-24 (3 stages * 8 LEDs)
    total_steps = 3 * NUM_LEDS
    position = int((adc_val / 65535) * total_steps)

    # Limit maximum value to prevent overflow
    if position > total_steps:
        position = total_steps

    for i in range(NUM_LEDS):
        # Logic judgment: priority from high to low (red -> green -> yellow)

        # Third part: Red overlay (when progress exceeds 16 + LED index)
        if position > (2 * NUM_LEDS + i):
            np[i] = COLOR_RED

        # Second part: Green overlay (when progress exceeds 8 + LED index)
        elif position > (1 * NUM_LEDS + i):
            np[i] = COLOR_GREEN

        # First part: Yellow lights up (when progress exceeds LED index)
        elif position > i:
            np[i] = COLOR_YELLOW

        # Other cases: Off
        else:
            np[i] = COLOR_OFF

    # Write data to LED strip
    np.write()

# --- Main program ---
print("System started: Potentiometer controls WS2812")

while True:
    try:
        # Read potentiometer analog value (16-bit unsigned integer: 0 - 65535)
        val = pot.read_u16()

        # Update lights
        update_leds(val)

        # Simple delay to prevent excessive refresh rate
        time.sleep_ms(50)

    except KeyboardInterrupt:
        # Turn off all LEDs when Ctrl+C is pressed
        for i in range(NUM_LEDS):
            np[i] = COLOR_OFF
        np.write()
        print("Program stopped")
        break