"""
BLE LED Control

Description: Receives commands via BLE to control an LED, allowing clients to turn it on or off remotely.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Bluetooth-Communication#ble-peripheral-received
"""

import aioble
import bluetooth
import machine
import uasyncio as asyncio

# Define UUIDs (use randomly generated UUIDs)
_SERVICE_UUID = bluetooth.UUID("48407a44-6e13-4d28-a559-210de862bc29")
_LED_CHAR_UUID = bluetooth.UUID("539ca2ac-09e5-49be-90da-3b157549eac3")

# Advertisement interval
_ADV_INTERVAL_US = 250_000

# Configure peripheral device
# read=True, write=True: Allow read and write
# capture=True: Allow aioble to capture write events for handling in code
led_service = aioble.Service(_SERVICE_UUID)
led_characteristic = aioble.Characteristic(
    led_service, _LED_CHAR_UUID, read=True, write=True, capture=True
)
aioble.register_services(led_service)

# Hardware initialization
led = machine.Pin(7, machine.Pin.OUT)
led.value(0)  # Default off

# Task: Handle write requests
async def led_task():
    print("LED task started")
    while True:
        # Wait for client to write data
        # written() returns a context manager that yields connection and value when a write occurs
        connection, value = await led_characteristic.written()

        print(f"Received: {value} from {connection.device}")

        if value:
            # Parse command (assuming 1 byte is sent)
            command = value[0]

            if command == 1:
                print("Turning LED ON")
                led.value(1)
            elif command == 0:
                print("Turning LED OFF")
                led.value(0)
            else:
                print(f"Unknown command: {command}")

            # Update characteristic value so clients can read the latest state
            led_characteristic.write(value)

# Task: Handle advertising (same as example 1)
async def peripheral_task():
    print("Advertising task started")
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_US,
            name="ESP32-LED",
            services=[_SERVICE_UUID],
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected()
            print("Disconnected")

# Main program entry
async def main():
    t1 = asyncio.create_task(led_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)

asyncio.run(main())