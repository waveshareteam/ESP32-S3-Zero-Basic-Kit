"""
Wi-Fi Scan

Description: Scans for available Wi-Fi networks in the vicinity and prints their details (SSID, RSSI, Channel, Encryption) to the console every 10 seconds.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/WiFi-Networking-Basic#wifi-scan
"""

import time
import network

def get_security_name(security_type):
    """Convert security type to readable string"""
    if security_type == 0:
        return "open"
    elif security_type == 1:
        return "WEP"
    elif security_type == 2:
        return "WPA-PSK"
    elif security_type == 3:
        return "WPA2-PSK"
    elif security_type == 4:
        return "WPA/WPA2-PSK"
    else:
        return "unknown"

# Create WLAN object in STA mode
wlan = network.WLAN(network.STA_IF)
# Activate WLAN interface
wlan.active(True)

print("Setup done")

while True:
    print("Scan start")
    # Scan for available Wi-Fi networks
    networks = wlan.scan()
    print("Scan done")

    if len(networks) == 0:
        print("no networks found")
    else:
        print(f"{len(networks)} networks found")
        print("Nr | SSID                             | RSSI | CH | Encryption")

        for i, net in enumerate(networks):
            # Network info format: (ssid, bssid, channel, RSSI, security, hidden)
            ssid = net[0].decode('utf-8') if net[0] else "Hidden"
            rssi = net[3]
            channel = net[2]
            security = net[4]

            # Format output
            print(f"{i+1:2d} | {ssid:32.32s} | {rssi:4d} | {channel:2d} | {get_security_name(security)}")

    print("")

    # Wait 10 seconds before next scan
    time.sleep(10)