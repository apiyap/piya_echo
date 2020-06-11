#!/usr/bin/env python
# Import necessary libraries.
import  Piya.Sonar.Echo as  pp

# Pin Numbering Modes
BOARD = 10
BCM = 11
TEGRA_SOC = 1000
CVM = 1001

# Define GPIO pin constants.
TRIGGER1_PIN = 11
ECHO1_PIN = 7

TRIGGER2_PIN = 12
ECHO2_PIN = 13


class Sonar2(object):
    def __init__(self):
        # Initialise Sensor with pins, speed of sound.
        self.speed_of_sound = 343       #m/s
        self.distance1 = 0
        self.distance2 = 0
        self.echo1 = pp.Echo(TRIGGER1_PIN, ECHO1_PIN, self.speed_of_sound, BOARD, True, self.echo1_callback)
        self.echo2 = pp.Echo(TRIGGER2_PIN, ECHO2_PIN, self.speed_of_sound, BOARD, True, self.echo2_callback)
        self.echo1.default_unit = 'cm'
        self.echo2.default_unit = 'cm'

    def echo1_callback(self,values):
        self.distance1 = values[0]
        #print("Distance:", self.distance1, self.echo1.default_unit  ,",",self.distance2 ,self.echo2.default_unit )
        
    def echo2_callback(self,values):
        self.distance2 = values[0]
        #print("Distance:", self.distance1, self.echo1.default_unit  ,",",self.distance2 ,self.echo2.default_unit )

    def run(self):
        try:
            while True:
                self.echo1.send()
                self.echo2.send()
                print("Distance:", self.distance1, self.echo1.default_unit  ,",",self.distance2 ,self.echo2.default_unit )
        
        finally:
            # Reset GPIO Pins.
            self.echo1.stop()
            self.echo2.stop()

sonars = Sonar2()
sonars.run()
