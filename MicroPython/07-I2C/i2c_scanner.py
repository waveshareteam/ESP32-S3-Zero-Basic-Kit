"""
I2C Scanner

Description: Scans the I2C bus for devices and prints their addresses.

Wiring:
- ESP32-S3-Zero
- SDA -> GPIO 2
- SCL -> GPIO 1

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/I2C-Communication#i2c-scanner
"""

from machine import Pin, I2C

# I2C pin definitions
SDA_PIN = 2
SCL_PIN = 1

# Initialize I2C
# id=0 uses the first hardware I2C controller
# scl=Pin(SCL_PIN), sda=Pin(SDA_PIN) specify pins
# freq=100000 sets I2C frequency to 100kHz (standard mode)
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)

print("Scanning I2C bus...")
devices = i2c.scan() # Scan for devices on bus

if len(devices) == 0:
    print("No I2C devices found")
else:
    print("I2C devices found:", len(devices))
    for device in devices:
        # Print decimal and hexadecimal addresses
        print("Decimal address: ", device, " | Hex address: ", hex(device))