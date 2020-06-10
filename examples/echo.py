#!/usr/bin/env python
# Import necessary libraries.
import  Piya.Sonar.Echo as  pp

# Pin Numbering Modes
BOARD = 10
BCM = 11
TEGRA_SOC = 1000
CVM = 1001

# Define GPIO pin constants.
TRIGGER_PIN = 11
ECHO_PIN = 7
# Initialise Sensor with pins, speed of sound.
speed_of_sound = 343       #m/s

def echo_callback(values):
    print("Distance:", values[0] ,"",echo.default_unit)

echo = pp.Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound, BOARD, True, echo_callback)
echo.default_unit = 'm'

# Take multiple measurements.
echo.read_loop()
# Reset GPIO Pins.
echo.stop()

