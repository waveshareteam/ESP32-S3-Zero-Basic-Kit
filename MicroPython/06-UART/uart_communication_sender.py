"""
UART Communication Sender

Description: 
    Sends commands via UART based on button presses.
    This code acts as the SENDER and requires `uart_communication_receiver.py` (Receiver) running on another ESP32-S3-Zero.

Wiring:
    Tips: The wiring connections are crossed (TX to RX, RX to TX).
    
    [Sender Device]              [Receiver Device]
    ESP32-S3-Zero                 ESP32-S3-Zero
    Button (GPIO 7)               LED (GPIO 7)
    TX (GPIO 12)       ------>    RX (GPIO 1)
    RX (GPIO 11)       <------    TX (GPIO 2)
    GND                <------>   GND

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/UART-Communication#esp32-uart-communication
"""

import time
from machine import Pin, UART

# Define pins
BUTTON_PIN = 7
TX_PIN = 12
RX_PIN = 11

# Configure UART1
# baudrate=9600: Baud rate
# tx=12, rx=11: Specify transmit and receive pins
uart = UART(1, baudrate=9600, tx=TX_PIN, rx=RX_PIN)

# Configure button pin (pull-up input)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

last_button_state = 1  # Initial state (pull-up defaults to 1)

print("Sender Ready. Press the button.")

while True:
    current_button_state = button.value()

    # Detect state change
    if current_button_state != last_button_state:
        if current_button_state == 0:
            # Button pressed (low level)
            # write() method sends byte data
            uart.write('1')
            print("Sent: 1 (Button Pressed)")
        else:
            # Button released (high level)
            uart.write('0')
            print("Sent: 0 (Button Released)")

        last_button_state = current_button_state
        time.sleep_ms(50)  # Simple debounce