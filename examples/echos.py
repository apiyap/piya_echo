# Import necessary libraries.
import sys
from Piya.Sonar.Echos import  Echos

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
    print(values)

pins = {"Echo1" : (TRIGGER1_PIN, ECHO1_PIN)
, "Echo2" : (TRIGGER2_PIN, ECHO2_PIN)
, "Echo3" : (TRIGGER3_PIN, ECHO3_PIN)
, "Echo4" : (TRIGGER4_PIN, ECHO4_PIN)
}
echos = Echos(pins, speed_of_sound, 3, BOARD, True, echo_callback)
echos.default_unit = 'cm'


print("Echo1 ready:", echos._echo_ready("Echo1"))
print("Echo2 ready:", echos._echo_ready("Echo2"))
print("Echo3 ready:", echos._echo_ready("Echo3"))
print("Echo4 ready:", echos._echo_ready("Echo4"))


echos.send()
echos.results()

# # Take multiple measurements.
echos.read_loop()
# # Reset GPIO Pins.
echos.stop()

