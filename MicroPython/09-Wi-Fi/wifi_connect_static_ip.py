"""
Wi-Fi Connect Static IP

Description: Connects to a specified Wi-Fi network using static IP configuration and prints the IP configuration to the console.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/WiFi-Networking-Basic#wifi-static-ip
"""

import time
import network

SSID = "Maker"         # Wi-Fi name
PASSWORD = "12345678"  # Wi-Fi password

# Configure static IP address, subnet mask, gateway, and DNS server
# Modify according to your actual LAN configuration
STATIC_IP = "192.168.137.100"  # Set static IP address
SUBNET = "255.255.255.0"       # Set subnet mask
GATEWAY = "192.168.137.1"      # Set gateway
DNS = "192.168.137.1"          # Set DNS server

# Create WLAN object in STA mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# Configure static IP
wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, DNS))

print(f"Connecting to {SSID}")

# Connect to the specified Wi-Fi network
wlan.connect(SSID, PASSWORD)

# Wait for connection to establish
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

print("")
print("WiFi connected.")
print(f"IP address: {wlan.ifconfig()[0]}")