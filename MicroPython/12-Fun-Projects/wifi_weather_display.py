"""
WiFi Weather Display

Description: Connects to Wi-Fi to fetch and display real-time weather from Seniverse API on a Waveshare 1.5-inch OLED.

Wiring:
- ESP32-S3-Zero
- OLED VCC -> 5V
- OLED GND -> GND
- OLED SCK -> GPIO 13
- OLED MOSI -> GPIO 11
- OLED CS -> GPIO 10
- OLED DC -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-6-Weather-Display
"""

import time
import network
import urequests
import json
from machine import Pin, SPI
import ssd1327

# Wi-Fi configuration
WIFI_SSID = "Maker"
WIFI_PASSWORD = "12345678"

# Seniverse weather API configuration (replace with your API key)
API_KEY = "your_api_key"
LOCATION = "shenzhen"  # City you want to query weather for

# API URL
API_URL = "https://api.seniverse.com/v3/weather/now.json?key={}&location={}&language=en&unit=c"

# Update interval (seconds)
UPDATE_INTERVAL = 1800  # 30 minutes

# SPI pin configuration
SCK_PIN = 13
MOSI_PIN = 11
CS_PIN = 10
DC_PIN = 8

# Initialize hardware SPI, use id=1, set clock frequency to 10 MHz
spi = SPI(1, baudrate=10000000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))

# For I2C interface, uncomment the following code
# from machine import I2C
# SDA_PIN = 2
# SCL_PIN = 1
# I2C_ADDR = 0x3d
# i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)

# Initialize display
try:
    # Using SPI interface
    oled = ssd1327.SSD1327_SPI(128, 128, spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN))

    # Using I2C interface
    # oled = ssd1327.SSD1327_I2C(128, 128, i2c, I2C_ADDR)

    print("OLED display initialized successfully.")
except Exception as e:
    print(f"Error initializing display: {e}")
    # If display initialization fails, program cannot continue
    while True:
        time.sleep(1)

def connect_wifi():
    """Connect to Wi-Fi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to network: {WIFI_SSID}...")
        oled.fill(0)
        oled.text("Connecting to", 5, 20, 15)
        oled.text("WiFi...", 5, 40, 15)
        oled.show()

        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # Wait for connection
        timeout = 15  # 15 second timeout
        start_time = time.time()
        while not wlan.isconnected() and (time.time() - start_time) < timeout:
            time.sleep(1)
            print(".", end="")

    if wlan.isconnected():
        print("\nNetwork connected!")
        print(f"IP Address: {wlan.ifconfig()[0]}")
        oled.fill(0)
        oled.text("WiFi Connected!", 5, 20, 15)
        oled.text("IP:", 5, 40, 15)
        oled.text(wlan.ifconfig()[0], 5, 55, 15)
        oled.show()
        time.sleep(2)
        return True
    else:
        print("\nFailed to connect to WiFi.")
        oled.fill(0)
        oled.text("WiFi Failed!", 5, 20, 15)
        oled.show()
        return False

def get_weather():
    """Fetch weather data from Seniverse API"""
    url = API_URL.format(API_KEY, LOCATION)
    print(f"Fetching weather from: {url}")

    try:
        response = urequests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            print("API Response:", weather_data)  # Uncomment for debugging

            # Extract required information from JSON data
            result = weather_data['results'][0]
            location_name = result['location']['name']
            weather_text = result['now']['text']
            temperature = result['now']['temperature']

            return location_name, weather_text, temperature

        else:
            print(f"Error getting weather: HTTP Status {response.status_code}")
            return None, f"HTTP Err {response.status_code}", ""

    except Exception as e:
        print(f"Error during API request: {e}")
        return None, "Request Error", ""

def display_weather(city, weather, temp):
    """Display weather information on OLED"""
    oled.fill(0)  # Clear screen

    # City name
    oled.text(f"City: {city}", 5, 10, 15)

    # Weather condition
    oled.text(f"Weather:", 5, 40, 15)
    oled.text(weather, 5, 55, 15)

    # Temperature
    oled.text(f"Temp: {temp} C", 5, 85, 15)

    oled.show()  # Update display
    print(f"Display updated: {city}, {weather}, {temp} C")

# Main program
def main():
    # First connect to Wi-Fi
    if not connect_wifi():
        # If connection fails, don't continue
        return

    while True:
        print("\n" + "="*20)
        oled.fill(0)
        oled.text("Fetching...", 5, 20, 15)
        oled.show()

        city, weather, temp = get_weather()

        if city:
            display_weather(city, weather, temp)
        else:
            # If fetch fails, display error message
            display_weather("Error", weather, temp)

        print(f"Waiting for {UPDATE_INTERVAL} seconds before next update...")
        time.sleep(UPDATE_INTERVAL)

# Run main program
if __name__ == "__main__":
    main()