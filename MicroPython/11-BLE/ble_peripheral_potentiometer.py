"""
BLE Potentiometer

Description: Reads potentiometer value via ADC and notifies connected BLE clients as a peripheral device.

Wiring:
- ESP32-S3-Zero
- Potentiometer -> GPIO 7

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/Bluetooth-Communication#ble-peripheral-sent
"""

import aioble
import bluetooth
import machine
import uasyncio as asyncio

# Define UUIDs (use randomly generated UUIDs)
_SERVICE_UUID = bluetooth.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
_POT_CHAR_UUID = bluetooth.UUID("1b9a473a-4493-4536-8b2b-9d4133488256")

# Advertisement interval
_ADV_INTERVAL_US = 250_000

# Configure peripheral device (GATT Server)
# Register service and characteristic
# read=True: Allow clients to read
# notify=True: Allow server to send notifications
pot_service = aioble.Service(_SERVICE_UUID)
pot_characteristic = aioble.Characteristic(
    pot_service, _POT_CHAR_UUID, read=True, notify=True
)
aioble.register_services(pot_service)

# Hardware initialization
pot = machine.ADC(machine.Pin(7))

# Task: Read sensor and update characteristic value
async def sensor_task():
    print("Sensor task started")
    last_val = -1

    while True:
        # Read potentiometer value (0-4095)
        val = pot.read()

        # Only update when value changes significantly (simple debounce/filter)
        if abs(val - last_val) > 10:
            last_val = val
            print(f"Potentiometer value: {val}")

            # Write characteristic value
            # Note: BLE data transmission uses byte strings, need to convert integer to bytes.
            # Here, convert 12-bit integer (0-4095) to 2-byte little-endian data
            encoded_val = val.to_bytes(2, "little")
            pot_characteristic.write(encoded_val)

            # Send notification to connected clients
            # notify only works when a client is connected and subscribed, aioble handles this automatically
            pot_characteristic.write(encoded_val, send_update=True)  # connection=None means notify all subscribed clients

        # Async delay to yield CPU to other tasks
        await asyncio.sleep_ms(100)

# Handle Bluetooth advertising and connections
async def peripheral_task():
    print("Advertising task started")
    while True:
        # Start advertising
        # name: Device name
        # services: List of service UUIDs included in the advertisement for client discovery
        async with await aioble.advertise(
            _ADV_INTERVAL_US,  # Advertisement interval (microseconds)
            name="ESP32_Potentiometer",
            services=[_SERVICE_UUID],
        ) as connection:
            print("Connection from", connection.device)
            # When a device connects, code blocks here until disconnection
            # During connection, sensor_task continues running in background updating data
            await connection.disconnected()
            print("Disconnected")

        # After disconnection, loop continues and resumes advertising

# Main program entry
async def main():
    # Run two tasks concurrently
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)

# Start asyncio event loop
asyncio.run(main())