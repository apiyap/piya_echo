# Copyright (c) 2020 Piya Pimchankam <piya.pimchankam@gmail.com>.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Python 2 & 3 print function compatibility
from __future__ import print_function

from time import time
from time import monotonic
from time import sleep
import Jetson.GPIO as GPIO
import threading
import numpy as np


class Echo(object):
    # Use over 50ms measurement cycle. 
    def __init__(self, trigger_pin, echo_pin, mPerSecond = 343, mIOMode=GPIO.BOARD, invert_echo_pin = False,callback=None):
        self._trigger_pin = trigger_pin # Trigger Pin
        self._echo_pin = echo_pin # Echo Pin
        self._gpio_mode = mIOMode
        self._mPerSecond = mPerSecond
        self._invert_echo_pin = invert_echo_pin
        self._call_back_fn = callback
        # How frequently are we going to send out a ping (in milliseconds). 50ms would be 20 times a second.
        self._sensor_rest = 0.05 # Sensor rest time between reads
        self._defaultUnit = 'cm'
        self._thread_running = False
        self._echo_times = np.array([0.0, 0.0])
        self._distance = 0.0
        self._thr = threading.Thread(target=self._echo_back)
        # Configure GPIO Pins
        try:
            # Use BOARD  pin numbering for the GPIO pins.
            
            GPIO.setmode(self._gpio_mode)
            GPIO.setup(self._trigger_pin, GPIO.OUT)
            GPIO.setup(self._echo_pin, GPIO.IN)      
            # Trigger 10us pulse for initial sensor cycling.
            GPIO.output(self._trigger_pin, False)
            sleep(0.5)
            GPIO.output(self._trigger_pin, True)
            sleep(0.00001)
            GPIO.output(self._trigger_pin, False)
            self._thread_running = True
            self._thr.start()
        except Exception as e:
            print(e)
        
    def __del__(self):
        self._thread_running = False
        # Reset GPIO settings
        

    def _echo_ready(self):
	    if self._invert_echo_pin :
		    return GPIO.input(self._echo_pin)

	    return not GPIO.input(self._echo_pin)

    def _echo_back(self):
        old_value=True
        check_value = False
        if self._invert_echo_pin :
            check_value = True

        while  self._thread_running :
            value = GPIO.input(self._echo_pin)
            if value != old_value :
                old_value = value
                self._echo_times[value] =  monotonic()
                #print("Echo [", value, "]:", self._echo_times[value])
                if value == check_value:
                    self._distance = self._valueToUnit(np.diff(self._echo_times), self._defaultUnit)
                    if self._call_back_fn!= None:
                        self._call_back_fn(self._distance)
                
            sleep(0.00001)
	
    """
    Convert echo time to distance unit of measure.
    """
    def _valueToUnit(self, value = 0.0, unit = 'cm'):
        if value > 0:
            if unit == 'mm':
                # return mm
                distance = (value * self._mPerSecond * 1000) / 2
            elif unit == 'cm':
                # return cm
                distance = (value * self._mPerSecond * 100) / 2
            elif unit == 'm':
                # return m
                distance = (value * self._mPerSecond) / 2
            elif unit == 'inch':
                # return inch
                distance = (value * self._mPerSecond * 39.3701) / 2
        else:
            distance = 0
            
        return distance

    def _trigger(self):
        # Trigger 10us pulse for initial sensor cycling.
        self._echo_times[0] = 0.0
        self._echo_times[1] = 0.0
        self._distance = 0.0
        GPIO.output(self._trigger_pin, True)
        sleep(0.00001)
        GPIO.output(self._trigger_pin, False)

    """
    For one shot distance measuring, first set the prefered units of
    measure (default = cm). Distance measurement will return zero
    if the sensor is not ready or timeout occurred.
    """
    def send(self):
        if self._echo_ready():
            self._trigger()
            sleep(self._sensor_rest)

        return self._distance

    def stop(self):
        self._thread_running = False
        

    def read_loop(self):
        try:
            while True:
                if self._echo_ready():
                    self._trigger()
                sleep(self._sensor_rest)
        finally:
            self.stop()
    
    """
    You can set the default units of measure for the send() and
    samples() methods. On class initialisation, cm is the default
    setting.
    """
    @property
    def default_unit(self):
        return self._defaultUnit

    
    @default_unit.setter
    def default_unit(self, unit):
        unitPass = False
        if unit == 'mm':
            unitPass = True
        elif unit == 'cm':
            unitPass = True
        elif unit == 'm':
            unitPass = True
        elif unit == 'inch':
            unitPass = True

        if unitPass == True:
            self._defaultUnit = unit
        else:
            raise RuntimeError("Incorrect Unit for Default Unit")


