"""
Wi-Fi Create AP Static IP

Description: Creates a Wi-Fi hotspot (Access Point) with static IP configuration and prints the IP configuration to the console.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/WiFi-Networking-Basic#wifi-static-ip
"""

import network

SSID = "ESP32-S3-TEST"  # Set hotspot name
PASSWORD = "12345678"   # Set hotspot password (at least 8 characters)

STATIC_IP = "192.168.5.1"      # Set static IP address
SUBNET = "255.255.255.0"       # Set subnet mask
GATEWAY = "192.168.5.1"        # Set gateway
DNS = "192.168.5.1"            # Set DNS server

# Create WLAN object in AP mode
ap = network.WLAN(network.AP_IF)
ap.active(True)

print("Configuring access point...")

# Configure static IP after activating interface
ap.ifconfig((STATIC_IP, SUBNET, GATEWAY, DNS))

# Configure and create hotspot
ap.config(essid=SSID, password=PASSWORD)

print(f"AP IP address: {ap.ifconfig()[0]}")
print("AP started")