"""
Wi-Fi Create AP

Description: Creates a Wi-Fi hotspot (Access Point) and prints the IP configuration to the console.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/WiFi-Networking-Basic#wifi-ap
"""

import network

SSID = "ESP32-S3-TEST"  # Set hotspot name
PASSWORD = "12345678"   # Set hotspot password (at least 8 characters)

# Create WLAN object in AP mode
ap = network.WLAN(network.AP_IF)
# Activate AP interface
ap.active(True)

print("Configuring access point...")

# Configure and create hotspot
ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)

# Get AP IP address
ip = ap.ifconfig()[0]
print(f"AP IP address: {ip}")
print("AP started")