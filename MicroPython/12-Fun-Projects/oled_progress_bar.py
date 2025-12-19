"""
OLED Progress Bar

Description: Reads potentiometer value via ADC and displays it as a progress bar or gauge on a Waveshare 1.5-inch OLED.

Wiring:
- ESP32-S3-Zero
- Potentiometer VCC -> 3.3V
- Potentiometer GND -> GND
- Potentiometer -> GPIO 7
- OLED VCC -> 5V
- OLED GND -> GND
- OLED SCK -> GPIO 13
- OLED MOSI -> GPIO 11
- OLED CS -> GPIO 10
- OLED DC -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-5-Progress-Bar
"""

import time
import math
from machine import Pin, SPI, ADC
import ssd1327

# SPI pin configuration
SCK_PIN = 13
MOSI_PIN = 11
CS_PIN = 10
DC_PIN = 8

# Potentiometer pin
POT_PIN = 7

# Initialize SPI
spi = SPI(1, baudrate=10000000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))
# Initialize OLED
oled = ssd1327.SSD1327_SPI(128, 128, spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN))

# For I2C, uncomment the following code
# from machine import I2C
# SDA_PIN = 2
# SCL_PIN = 1
# I2C_ADDR = 0x3d
# i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
# oled = ssd1327.SSD1327_I2C(128, 128, i2c, I2C_ADDR)

# Initialize ADC
adc = ADC(Pin(POT_PIN))

def get_percentage():
    """Read potentiometer and return value as 0-100 integer"""
    val = adc.read_u16()  # 0-65535
    percent = int((val / 65535) * 100)
    return max(0, min(100, percent))

# Effect function 1: Horizontal progress bar
def show_horizontal_bar(oled, percent):
    """
    Draw horizontal progress bar
    """
    oled.fill(0)  # Clear buffer

    # Layout parameters
    bar_x = 10
    bar_y = 55
    bar_w = 108
    bar_h = 18

    # 1. Draw border (using gray, color value 6)
    # Note: Using framebuf.rect
    oled.framebuf.rect(bar_x, bar_y, bar_w, bar_h, 6)

    # 2. Draw inner fill (using bright white, color value 15)
    # Calculate fill width, with 2-pixel margin
    inner_max_w = bar_w - 4
    fill_w = int((percent / 100) * inner_max_w)

    if fill_w > 0:
        oled.framebuf.fill_rect(bar_x + 2, bar_y + 2, fill_w, bar_h - 4, 15)

    # 3. Draw text
    oled.text("Progress", 32, 35, 8)  # Title

    p_str = f"{percent}%"
    # Simple center calculation: screen width 128, assuming character width 8
    text_x = 64 - (len(p_str) * 4)
    oled.text(p_str, text_x, 80, 15)  # Value

    oled.show()  # Refresh display

# Effect function 2: Semi-circular gauge
def show_gauge(oled, percent):
    """
    Draw semi-circular gauge
    """
    oled.fill(0)  # Clear buffer

    # Gauge parameters
    cx, cy = 64, 105  # Center position (bottom center of screen)
    radius = 55       # Radius
    pointer_len = 48  # Pointer length

    # 1. Draw scale marks (simulating semicircle)
    # Angle range: 180 degrees (left) -> 0 degrees (right)
    for i in range(0, 11):  # 0 to 10, total 11 major marks
        angle = 180 - (i * 18)
        rad = math.radians(angle)

        # Outer point
        x1 = int(cx + math.cos(rad) * radius)
        y1 = int(cy - math.sin(rad) * radius)

        # Inner point (mark length 5)
        x2 = int(cx + math.cos(rad) * (radius - 6))
        y2 = int(cy - math.sin(rad) * (radius - 6))

        oled.line(x1, y1, x2, y2, 6)  # Color 6 (gray)

    # 2. Draw pointer
    # Calculate angle for current value
    current_angle = 180 - (percent / 100 * 180)
    current_rad = math.radians(current_angle)

    px = int(cx + math.cos(current_rad) * pointer_len)
    py = int(cy - math.sin(current_rad) * pointer_len)

    oled.line(cx, cy, px, py, 15)  # Color 15 (bright)

    # 3. Draw center decoration
    oled.framebuf.fill_rect(cx-2, cy-2, 5, 5, 15)

    # 4. Bottom text
    oled.text(f"{percent}", 56, 110, 15)
    oled.text("GAUGE", 44, 10, 8)

    oled.show()  # Refresh display

# ================= Main loop =================

print("Started.")

while True:
    # Read data
    val = get_percentage()

    # Select display mode (uncomment the one you need)

    # Mode A: Horizontal progress bar
    show_horizontal_bar(oled, val)

    # Mode B: Semi-circular gauge
    # show_gauge(oled, val)

    # Simple delay to prevent excessive refresh rate
    time.sleep(0.05)