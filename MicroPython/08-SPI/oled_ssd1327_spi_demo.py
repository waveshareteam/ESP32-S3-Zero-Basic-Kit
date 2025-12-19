"""
OLED SSD1327 SPI Demo

Description: Demonstrates drawing text and shapes on an SSD1327 OLED via SPI.

Dependencies: This code requires the ssd1327.py library file.

Wiring:
- ESP32-S3-Zero
- OLED VCC -> 3.3V
- OLED GND -> GND
- OLED SCK -> GPIO 13
- OLED MOSI -> GPIO 11
- OLED CS -> GPIO 10
- OLED DC -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/SPI-Communication
"""

from machine import Pin, SPI
import ssd1327

# SPI pin configuration
SCK_PIN = 13
MOSI_PIN = 11
CS_PIN = 10
DC_PIN = 8

# Initialize hardware SPI
# Use id=1 (HSPI), set clock frequency to 10 MHz
spi = SPI(1, baudrate=10000000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))

# Initialize display
oled = ssd1327.SSD1327_SPI(128, 128, spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN))

print("SSD1327 OLED test")

# Clear screen (fill with black)
oled.fill(0)

# Display text
# framebuf.text(s, x, y, c)
# c is the color value, for 4-bit grayscale, range is 0-15. 15 is brightest, 0 is black.
oled.text("Hello,", 10, 10, 15)
oled.text("MicroPython!", 10, 25, 8)
oled.text("ESP32", 10, 40, 1)  # Lower brightness text

# Draw graphics using framebuf
# Draw rectangle border
oled.framebuf.rect(0, 0, 128, 128, 15)
# Draw circle or ellipse
oled.framebuf.ellipse(0, 0, 128, 128, 15)

# Refresh display
oled.show()


