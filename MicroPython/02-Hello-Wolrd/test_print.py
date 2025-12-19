"""
Hello World Loop

Description: Prints CPU frequency and a 'Hello World' counter every second.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Basic
"""

import sys
import machine
import time

# Get and print CPU frequency (convert to MHz)
freq = machine.freq() / 1000000
print(f"Device Info: {sys.platform}\nCPU Freq: {freq} MHz")

count = 0

try:
    while True:
        # Print current count value
        print(f"Hello World! {count}")
        count += 1
        # Wait for 1 second
        time.sleep(1)
except KeyboardInterrupt:
    # Execute when keyboard interrupt (CTRL+C) is detected
    print("Exit")