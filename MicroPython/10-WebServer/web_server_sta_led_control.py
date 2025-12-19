"""
Web Server STA LED Control

Description: Web server in Station (STA) mode for LED control. Connects to Wi-Fi and provides a web interface to toggle an LED (GPIO 7).

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Web-Server#web-server-led-sta
"""

import time
import network
import socket
from machine import Pin

# LED configuration
led = Pin(7, Pin.OUT)
led.value(0)  # Initially off

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
    if led.value() == 1:
        gpio_state = "ON"
        button_html = '<a href="/ledoff">Turn off the LED</a>'
    else:
        gpio_state = "OFF"
        button_html = '<a href="/ledon">Turn on the LED</a>'
        
    html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ESP32S3 Test</title>
</head>
<body><h1>ESP32 Web Server</h1>
<p>GPIO state: <strong>""" + gpio_state + """</strong></p>
""" + button_html + """
</body></html>"""
    return html

# Connect to Wi-Fi
connect_wifi()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print("Web server is running...")

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))

        request = conn.recv(1024)
        request = str(request)
        # View network request
        # print(request)

        if 'GET /ledon' in request:
            print('LED ON')
            led.value(1)
        elif 'GET /ledoff' in request:
            print('LED OFF')
            led.value(0)

        # Prepare and send web page response
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        
    except OSError as e:
        conn.close()
        print('Connection closed')