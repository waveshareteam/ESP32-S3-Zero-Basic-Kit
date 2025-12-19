
"""
Web Server STA Basic

Description: Basic web server example in Station (STA) mode. Connects to an existing Wi-Fi network and serves a simple 'Hello World' HTML page.

Wiring:
- ESP32-S3-Zero

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Web-Server#web-server-sta
"""

import time
import network
import socket
from machine import Pin

# Wi-Fi configuration
SSID = "Maker"         # Replace with your Wi-Fi name
PASSWORD = "12345678"  # Replace with your Wi-Fi password

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
            print('.', end='')
    print('\nNetwork connected')
    print('IP address:', wlan.ifconfig()[0])
    return wlan

def web_page():
    html = """<!DOCTYPE html> <html>
<head><meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1">
<title>ESP32 MicroPython Web Server</title>
</head><body>
<h1>Hello World!</h1>
<p>Hello from ESP32 MicroPython</p>
</body></html>
"""
    return html

# Connect to Wi-Fi
connect_wifi()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind to port 80
s.bind(('', 80))
# Start listening
s.listen(5)

print("Web server is running...")

while True:
    try:
        # Accept client connection
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))

        # Receive request
        request = conn.recv(1024)
        # print('Content = %s' % str(request))  # For debugging, print full request header

        # Send response
        response = web_page()

        # Send HTTP response headers
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')

        # Send HTML content
        conn.sendall(response)

        # Close connection
        conn.close()
        
    except OSError as e:
        conn.close()
        print('Connection closed')