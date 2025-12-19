"""
Potentiometer Reader

Description: Reads and prints the raw ADC value and calculated voltage from a potentiometer.

Wiring:
- ESP32-S3-Zero
- Potentiometer VCC -> 3.3V
- Potentiometer GND -> GND
- Potentiometer -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Analog-Input
"""

import time
from machine import Pin, ADC

# Define potentiometer pin (GPIO 7)
POT_PIN = 7

# Initialize ADC
# 1. Create ADC object associated with pin
pot = ADC(Pin(POT_PIN))

while True:
    # Read raw analog value (0 - 4095)
    adc_value = pot.read()

    # Read voltage value (in microvolts uV) and convert to millivolts (mV)
    voltage_uv = pot.read_uv()
    voltage_mv = voltage_uv / 1000

    # Format output for viewing in plotter
    # Format: Label:Value
    print("ADC:", adc_value, ",Voltage_mV:", voltage_mv)

    # Delay 0.1 seconds
    time.sleep(0.1)