"""
OLED SSD1327 I2C Demo

Description: Demonstrates drawing text and shapes on an SSD1327 OLED via I2C.

Dependencies: This code requires the ssd1327.py library file.

Wiring:
- ESP32-S3-Zero
- OLED VCC -> 3.3V
- OLED GND -> GND
- OLED (SSD1327) SDA -> GPIO 2
- OLED (SSD1327) SCL -> GPIO 1

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/I2C-Communication#i2c-ssd1327
"""

from machine import I2C, Pin
import ssd1327

# Pin definitions
SDA_PIN = 2
SCL_PIN = 1
I2C_ADDR = 0x3d

# Initialize I2C
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)

# Initialize OLED
oled = ssd1327.SSD1327_I2C(128, 128, i2c, I2C_ADDR)

# Clear screen (fill with black)
oled.fill(0)

# Display text
# framebuf.text(s, x, y, c)
# c is color value, for 4-bit grayscale range is 0-15. 15 is brightest, 0 is black.
oled.text("Hello,", 10, 10, 15)
oled.text("MicroPython!", 10, 25, 8)
oled.text("ESP32", 10, 40, 1) # Lower brightness text

# Draw graphics using framebuf
# Draw rectangle outline
oled.framebuf.rect(0, 0, 128, 128, 15)
# Draw circle or ellipse
oled.framebuf.ellipse(0, 0, 128, 128, 15)

# Refresh display
oled.show()