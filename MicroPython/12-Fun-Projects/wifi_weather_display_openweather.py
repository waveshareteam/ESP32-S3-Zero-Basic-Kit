"""
WiFi Weather Display (OpenWeather)

Description: Connects to Wi-Fi to fetch and display real-time weather from OpenWeather API on a Waveshare 1.5-inch OLED.

Dependencies: This code requires the ssd1327.py library file.

Wiring:
- ESP32-S3-Zero
- OLED VCC  -> 3.3V
- OLED GND  -> GND
- OLED SCK  -> GPIO 13
- OLED MOSI -> GPIO 11
- OLED CS   -> GPIO 10
- OLED DC   -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-6-Weather-Display
- Tutorial [EN]: https://docs.waveshare.com/ESP32-MicroPython-Tutorials/12-6-Weather-Display
"""

import time
import network
import urequests
import json
from machine import Pin, SPI
import ssd1327

# Wi-Fi Configuration
WIFI_SSID = "Maker"
WIFI_PASSWORD = "12345678"

# OpenWeatherMap API Configuration (Please replace with your private key)
API_KEY = "your_api_key"

# City to query (e.g., "Shenzhen", "New%20York,US", "London", "Stockholm")
LOCATION = "Stockholm"

# API URL
API_URL = "http://api.openweathermap.org/data/2.5/weather?appid={}&q={}&units=metric"

# Update Interval (seconds)
UPDATE_INTERVAL = 1800  # 30 minutes

# Display Text Brightness (0-15)
TEXT_BRIGHTNESS = 8

# SPI Pin Configuration
SCK_PIN = 13
MOSI_PIN = 11
CS_PIN = 10
DC_PIN = 8
RST_PIN = 9

# Initialize hardware SPI, using id=1, set clock frequency to 10 MHz
spi = SPI(1, baudrate=10000000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))

# Initialize the display
try:
    # Using SPI interface
    oled = ssd1327.SSD1327_SPI(128, 128, spi, dc=Pin(DC_PIN), res=Pin(RST_PIN), cs=Pin(CS_PIN))
    print("OLED display initialized successfully.")
except Exception as e:
    print(f"Error initializing display: {e}")
    # If the display initialization fails, the program cannot continue
    while True:
        time.sleep(1)

def connect_wifi():
    """Connect to the Wi-Fi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to network: {WIFI_SSID}...")
        oled.fill(0)
        oled.text("Connecting to", 5, 20, TEXT_BRIGHTNESS)
        oled.text("WiFi...", 5, 40, TEXT_BRIGHTNESS)
        oled.show()
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        # Wait for the connection to succeed
        timeout = 15  # 15-second timeout
        start_time = time.time()
        while not wlan.isconnected() and (time.time() - start_time) < timeout:
            time.sleep(1)
            print(".", end="")
    if wlan.isconnected():
        print("\nNetwork connected!")
        print(f"IP Address: {wlan.ifconfig()[0]}")
        oled.fill(0)
        oled.text("WiFi Connected!", 5, 20, TEXT_BRIGHTNESS)
        oled.text("IP:", 5, 40, TEXT_BRIGHTNESS)
        oled.text(wlan.ifconfig()[0], 5, 55, TEXT_BRIGHTNESS)
        oled.show()
        time.sleep(2)
        return True
    else:
        print("\nFailed to connect to WiFi.")
        oled.fill(0)
        oled.text("WiFi Failed!", 5, 20, TEXT_BRIGHTNESS)
        oled.show()
        return False

def get_weather():
    """Fetch weather data from the OpenWeatherMap API"""
    url = API_URL.format(API_KEY, LOCATION)
    print(f"Fetching weather from: {url}")
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            print("API Response:", weather_data)
            # Extract required information from JSON data
            location_name = weather_data['name']
            weather_text = weather_data['weather'][0]['main']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            return location_name, weather_text, temperature, humidity
        else:
            print(f"Error getting weather: HTTP Status {response.status_code}")
            return None, f"HTTP Err {response.status_code}", "", ""
    except Exception as e:
        print(f"Error during API request: {e}")
        return None, "Request Error", "", ""

def display_weather(city, weather, temp, hum):
    """Display weather information on the OLED"""
    oled.fill(0) # Clear the screen
    # City name
    oled.text(f"City: {city}", 5, 10, TEXT_BRIGHTNESS)
    # Weather condition
    oled.text(f"Weather:", 5, 40, TEXT_BRIGHTNESS)
    oled.text(str(weather), 5, 55, TEXT_BRIGHTNESS)
    # Temperature
    oled.text(f"Temp: {temp} C", 5, 80, TEXT_BRIGHTNESS)
    # Humidity
    oled.text(f"Hum:  {hum} %", 5, 100, TEXT_BRIGHTNESS)
    oled.show() # Update the display
    print(f"Display updated: {city}, {weather}, {temp} C, {hum}%")

def display_error(message, detail):
    """Display error information on the OLED"""
    oled.fill(0)
    oled.text(f"Error:", 5, 20, TEXT_BRIGHTNESS)
    oled.text(f"{message}", 5, 30, TEXT_BRIGHTNESS)
    oled.text(f"Detail: ", 5, 50, TEXT_BRIGHTNESS)
    oled.text(f"{detail}", 5, 60, TEXT_BRIGHTNESS)
    oled.show()
    print(f"Error displayed: {message}, {detail}")

# Main Program
def main():
    # First, connect to Wi-Fi
    if not connect_wifi():
        # If the connection fails, do not continue
        return
    while True:
        print("\n" + "="*20)
        oled.fill(0)
        oled.text("Fetching...", 5, 20, TEXT_BRIGHTNESS)
        oled.show()
        city, weather, temp, hum = get_weather()
        if city:
            display_weather(city, weather, temp, hum)
        else:
            # If fetching fails, display an error message
            display_error("API Error", weather)
        print(f"Waiting for {UPDATE_INTERVAL} seconds before next update...")
        time.sleep(UPDATE_INTERVAL)

# Run the main program
if __name__ == "__main__":
    main()
