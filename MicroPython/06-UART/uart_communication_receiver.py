"""
UART Communication Receiver

Description: 
    Receives commands via UART to control an LED.
    This code acts as the RECEIVER and requires `uart_communication_sender.py` (Sender) running on another ESP32-S3-Zero.

Wiring:
    Tips: The wiring connections are crossed (RX to TX, TX to RX).

    [Receiver Device]            [Sender Device]
    ESP32-S3-Zero                 ESP32-S3-Zero
    LED (GPIO 7)                  Button (GPIO 7)
    RX (GPIO 1)        <------    TX (GPIO 12)
    TX (GPIO 2)        ------>    RX (GPIO 11)
    GND                <------>   GND

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/UART-Communication#esp32-uart-communication
"""

import time
from machine import Pin, UART

# Define pins
LED_PIN = 7
RX_PIN = 1
TX_PIN = 2

# Configure UART1
# Note: Receiver RX connects to sender TX, receiver TX connects to sender RX
# According to wiring diagram: RX=1, TX=2
uart = UART(1, baudrate=9600, tx=TX_PIN, rx=RX_PIN)

# Configure LED pin
led = Pin(LED_PIN, Pin.OUT)

print("Receiver Ready. Waiting for commands...")

while True:
    # any() returns number of characters in receive buffer, >0 means data available
    if uart.any():
        # read(1) reads 1 byte
        command = uart.read(1)

        # Note: read() returns bytes object (e.g. b'1')
        if command == b'1':
            led.value(1)
            print("Received: 1 -> LED ON")
        elif command == b'0':
            led.value(0)
            print("Received: 0 -> LED OFF")

    time.sleep_ms(10) # Small delay to avoid excessive CPU usage