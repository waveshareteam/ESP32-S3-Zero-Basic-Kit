"""
Traffic Light Simulation

Description: Simulates a traffic light sequence: green, blinking yellow, and red.

Wiring:
- Board: Waveshare ESP32-S3-Zero
- Red LED -> GPIO 7
- Yellow LED -> GPIO 8
- Green LED -> GPIO 9

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-1-Traffic-Light
"""

import time
import machine

# Define GPIO pins for red, yellow, and green lights
RED_LED_PIN = 7
YELLOW_LED_PIN = 8
GREEN_LED_PIN = 9

# Define duration for each light color
RED_LIGHT_DURATION = 10     # Red light on for 10 seconds
GREEN_LIGHT_DURATION = 8    # Green light on for 8 seconds
YELLOW_LIGHT_DURATION = 3   # Yellow light phase lasts 3 seconds total
YELLOW_BLINK_INTERVAL = 0.5 # Yellow light blink interval

# Initialize LED pins as output
red_led = machine.Pin(RED_LED_PIN, machine.Pin.OUT)
yellow_led = machine.Pin(YELLOW_LED_PIN, machine.Pin.OUT)
green_led = machine.Pin(GREEN_LED_PIN, machine.Pin.OUT)

def all_lights_off():
    """A helper function to turn off all lights."""
    red_led.off()
    yellow_led.off()
    green_led.off()

# Program start
print("Traffic light simulation started...")
print(f"Config: Red={RED_LIGHT_DURATION}s, Green={GREEN_LIGHT_DURATION}s, Yellow={YELLOW_LIGHT_DURATION}s")
print(f"Yellow blink interval: {YELLOW_BLINK_INTERVAL}s")

try:
    # Create infinite loop to simulate continuous traffic light operation
    while True:
        # --- Green light phase ---
        print("Green light on")
        all_lights_off()  # Turn off all lights first to ensure clean state
        green_led.on()    # Turn on green light
        time.sleep(GREEN_LIGHT_DURATION)  # Wait for green light duration

        # --- Yellow light blinking phase ---
        print("Yellow light blinking")
        green_led.off()  # Turn off green light

        # Calculate number of blinks within yellow light duration
        # One complete blink cycle is (on + off), duration is YELLOW_BLINK_INTERVAL * 2
        # Total duration divided by single cycle duration gives number of blinks
        num_blinks = int(YELLOW_LIGHT_DURATION / (YELLOW_BLINK_INTERVAL * 2))

        # Ensure at least one blink even if total time is very short
        if num_blinks == 0:
            num_blinks = 1

        for _ in range(num_blinks):
            yellow_led.on()   # Turn on yellow light
            time.sleep(YELLOW_BLINK_INTERVAL)  # On for a while
            yellow_led.off()  # Turn off yellow light
            time.sleep(YELLOW_BLINK_INTERVAL)  # Off for a while

        # Ensure yellow light is off before entering red light phase
        yellow_led.off()

        # --- Red light phase ---
        print("Red light on")
        # Yellow and green lights already off, just turn on red light
        red_led.on()
        time.sleep(RED_LIGHT_DURATION)  # Wait for red light duration

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

finally:
    # Ensure all lights are off whether program ends normally or is interrupted
    all_lights_off()
    print("All traffic lights off, program ended.")