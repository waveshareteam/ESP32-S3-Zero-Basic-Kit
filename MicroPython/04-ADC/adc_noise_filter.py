"""
ADC Noise Filter

Description: Reads ADC values multiple times and calculates the average after removing outliers.

Wiring:
- ESP32-S3-Zero
- Potentiometer -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Analog-Input#reduce-adc-noise
"""

import time
from machine import Pin, ADC

POT_PIN = 7

pot = ADC(Pin(POT_PIN))

def read_average_adc(adc_obj, times=10):
    """
    Read ADC values multiple times, remove max and min, then calculate average
    :param adc_obj: ADC object
    :param times: Number of samples, default is 10
    :return: Averaged integer value
    """
    val_list = []
    for _ in range(times):
        val_list.append(adc_obj.read())
        time.sleep_ms(1) # Sampling interval

    # Remove max and min values, calculate average of remaining data
    if len(val_list) > 2:
        val_list.remove(min(val_list))
        val_list.remove(max(val_list))

    return int(sum(val_list) / len(val_list))

while True:
    # Get average of 20 samples
    smooth_value = read_average_adc(pot, 20)

    print("Raw:", pot.read(), "Smooth:", smooth_value)
    time.sleep(0.1)