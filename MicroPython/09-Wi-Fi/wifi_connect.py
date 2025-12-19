"""
Wi-Fi Connect

Description: Connects to a specified Wi-Fi network and prints the IP configuration to the console.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/WiFi-Networking-Basic#wifi-sta
"""

import time
import network

# Replace with your actual Wi-Fi network credentials
SSID = "Maker"        # Replace with your Wi-Fi name
PASSWORD = "12345678"  # Replace with your Wi-Fi password

# Create WLAN object in STA mode
wlan = network.WLAN(network.STA_IF)
# Activate WLAN interface
wlan.active(True)

print(f"Connecting to {SSID}")

# Connect to the specified Wi-Fi network
wlan.connect(SSID, PASSWORD)

# Wait for connection to establish
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

print("")
print("WiFi connected.")
print("IP config:", wlan.ifconfig())