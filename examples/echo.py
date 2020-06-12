# Import necessary libraries.
import sys
from Piya.Sonar.Echo import  Echo

# Pin Numbering Modes
BOARD = 10
BCM = 11
TEGRA_SOC = 1000
CVM = 1001


TRIGGER1_PIN = 11
ECHO1_PIN = 7

TRIGGER2_PIN = 12
ECHO2_PIN = 13

TRIGGER3_PIN = 15
ECHO3_PIN = 16

TRIGGER4_PIN = 19
ECHO4_PIN = 18

# Define GPIO pin constants.
TRIGGER_PIN = TRIGGER4_PIN
ECHO_PIN = ECHO4_PIN
# Initialise Sensor with pins, speed of sound.
speed_of_sound = 343       #m/s

def echo_callback(values):
    print("Distance:", values[0] ,"",echo.default_unit)

echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound, 3, BOARD, True, echo_callback)
echo.default_unit = 'cm'

# Take multiple measurements.
echo.read_loop()
# Reset GPIO Pins.
echo.stop()

