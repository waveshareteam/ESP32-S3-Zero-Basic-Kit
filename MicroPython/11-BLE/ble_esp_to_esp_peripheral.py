"""
BLE ESP to ESP Peripheral

Description: Peripheral device that receives PWM data via BLE from a central ESP32 (running ble_esp_to_esp_central.py) to adjust LED brightness.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Bluetooth-Communication#ble-between-esp32
"""

import aioble
import bluetooth
import machine
import uasyncio as asyncio
import struct

# Define UUIDs
_SERVICE_UUID = bluetooth.UUID("458063a1-02bf-4664-857e-16c1030be066")
_BRIGHTNESS_CHAR_UUID = bluetooth.UUID("a5209632-66a9-411d-9353-9be5507790fa")

# Advertisement interval
_ADV_INTERVAL_US = 250_000

# Configure peripheral device
# capture=True: Allow aioble to capture write events
led_service = aioble.Service(_SERVICE_UUID)
led_characteristic = aioble.Characteristic(
    led_service, _BRIGHTNESS_CHAR_UUID, read=True, write=True, capture=True
)
aioble.register_services(led_service)

# Hardware initialization
led = machine.PWM(machine.Pin(7))
led.freq(1000)
led.duty_u16(0)

# Task: Handle write requests
async def led_task():
    print("LED task started")
    while True:
        connection, value = await led_characteristic.written()

        if value:
            # Received value is 0-65535 (2 bytes, little-endian)
            try:
                duty_u16 = struct.unpack("<H", value)[0]
                print(f"Received duty: {duty_u16}")

                # Set PWM duty cycle directly
                led.duty_u16(duty_u16)

                # Update characteristic value
                led_characteristic.write(value)
            except:
                pass

# Task: Handle advertising
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