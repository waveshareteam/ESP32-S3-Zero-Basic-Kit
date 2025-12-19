"""
BLE ESP to ESP Central

Description: Central device that reads potentiometer data and sends it via BLE to a peripheral ESP32 (running ble_esp_to_esp_peripheral.py) to control LED brightness.

Wiring:
- ESP32-S3-Zero
- Potentiometer -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Bluetooth-Communication#ble-between-esp32
"""

import aioble
import bluetooth
import machine
import uasyncio as asyncio
import struct

# Define target UUIDs
_SERVICE_UUID = bluetooth.UUID("458063a1-02bf-4664-857e-16c1030be066")
_BRIGHTNESS_CHAR_UUID = bluetooth.UUID("a5209632-66a9-411d-9353-9be5507790fa")

# Hardware initialization
pot = machine.ADC(machine.Pin(7))

# Helper function: Find and connect to device
async def find_device():
    print(f"Scanning for UUID: {_SERVICE_UUID} ...")
    # Scan for 5 seconds
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # Check service UUID
            if _SERVICE_UUID in result.services():
                device_name = result.name() or "Unknown"
                print(f"Found Target Device: {device_name}")
                return result.device
    return None

# Main task
async def central_task():
    print("Central task started")

    while True:
        device = await find_device()
        if not device:
            print("Device not found, retrying...")
            await asyncio.sleep_ms(1000)
            continue

        try:
            print(f"Connecting to device...")
            connection = await device.connect(timeout_ms=5000)
        except asyncio.TimeoutError:
            print("Connection timeout")
            continue

        async with connection:
            print("Connected")

            try:
                # Discover services
                print("Discovering services...")
                service = await connection.service(_SERVICE_UUID)
                if not service:
                    print("Service not found")
                    continue

                # Discover characteristics
                print("Discovering characteristics...")
                char = await service.characteristic(_BRIGHTNESS_CHAR_UUID)
                if not char:
                    print("Characteristic not found")
                    continue

                print("Ready to send data")
                last_val = -1

                while True:
                    # Read potentiometer (0-65535)
                    val = pot.read_u16()

                    # Only send when change exceeds threshold to avoid jitter
                    if abs(val - last_val) > 1000:
                        last_val = val
                        print(f"Sending duty: {val}")

                        # Write data (2 bytes, little-endian)
                        await char.write(struct.pack("<H", val), response=False)

                    await asyncio.sleep_ms(100)

            except Exception as e:
                print(f"Error: {e}")

            print("Disconnected")
            # Loop back to start, rescan and reconnect

# Main program entry
asyncio.run(central_task())