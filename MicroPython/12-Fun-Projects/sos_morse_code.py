"""
SOS Morse Code Simulation

Description: Simulates sending SOS Morse code using an LED and buzzer.

Wiring:
- ESP32-S3-Zero
- LED -> GPIO 7
- Buzzer -> GPIO 8

Link:
- Tutorial [ZH]: https://docs.waveshare.net/ESP32-MicroPython-Tutorials/12-2-SOS
"""

# Import required libraries
import time
import machine

# Define pins for LED and buzzer
LED_PIN = 7     # LED
BUZZER_PIN = 8  # Buzzer

# Configure pins as output
led = machine.Pin(LED_PIN, machine.Pin.OUT)
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

# --- Morse code timing definitions ---
DOT_DURATION = 0.2  # "Dot" duration (seconds), basic time unit

DASH_DURATION = 3 * DOT_DURATION       # Dash = 3 dots
INTER_ELEMENT_GAP = DOT_DURATION       # Gap between elements = 1 dot
INTER_LETTER_GAP = 3 * DOT_DURATION    # Gap between letters = 3 dots
INTER_WORD_GAP = 7 * DOT_DURATION      # Gap between words = 7 dots

# --- Core functions ---

def signal_on():
    """Turn on both LED and buzzer"""
    led.on()
    buzzer.on()

def signal_off():
    """Turn off both LED and buzzer"""
    led.off()
    buzzer.off()

def dot():
    """Send a dot signal"""
    signal_on()
    time.sleep(DOT_DURATION)
    signal_off()

def dash():
    """Send a dash signal"""
    signal_on()
    time.sleep(DASH_DURATION)
    signal_off()

def letter_s():
    """Send letter 'S' (...): Three dots"""
    print('.', end='')
    dot()
    time.sleep(INTER_ELEMENT_GAP)
    print('.', end='')
    dot()
    time.sleep(INTER_ELEMENT_GAP)
    print('.', end='')
    dot()

def letter_o():
    """Send letter 'O' (---): Three dashes"""
    print('-', end='')
    dash()
    time.sleep(INTER_ELEMENT_GAP)
    print('-', end='')
    dash()
    time.sleep(INTER_ELEMENT_GAP)
    print('-', end='')
    dash()

def play_sos():
    """Play complete SOS signal sequence"""

    print("Sending S: ", end='')
    letter_s()
    print(" | ", end='')
    time.sleep(INTER_LETTER_GAP)

    print("Sending O: ", end='')
    letter_o()
    print(" | ", end='')
    time.sleep(INTER_LETTER_GAP)

    print("Sending S: ", end='')
    letter_s()
    print()
    print("SOS sequence complete.")

# --- Main program ---
try:
    print("Program started, ready to send SOS signal. Press Ctrl+C to stop.")
    # Ensure devices are off initially
    signal_off()
    time.sleep(2)  # Wait 2 seconds before starting

    # Infinite loop, continuously send SOS signal
    while True:
        play_sos()

        # Wait after each complete SOS sequence
        print(f"Waiting {INTER_WORD_GAP} seconds before repeat...\n")
        time.sleep(INTER_WORD_GAP)

except KeyboardInterrupt:
    # Catches KeyboardInterrupt when user presses Ctrl+C
    print("\nProgram interrupted by user.")

finally:
    # Execute this code whether program ends normally or is interrupted
    print("Turning off LED and buzzer...")
    signal_off()
    print("Devices safely shut down.")