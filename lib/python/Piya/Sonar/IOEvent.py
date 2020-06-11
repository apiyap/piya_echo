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
from time import perf_counter
import Jetson.GPIO as GPIO
from threading import Thread, Lock


class IOEvent(Thread):
    def __init__(self, event, io_pin = 7 ,max_timeout = 10 ):
        Thread.__init__(self)
        self._stopped = event
        self._io_pin = io_pin
        self._output_pin = 11
        self._max_timeout = max_timeout
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._io_pin, GPIO.IN)
        GPIO.setup(self._output_pin, GPIO.OUT, initial=GPIO.HIGH)
        
    def __del__(self):
        self._thread_running = False
        # Reset GPIO settings

    def run(self):
        old_value=True

        while not self._stopped.is_set():
            value = GPIO.input(self._io_pin)
            if value != old_value :
                old_value = value
                print("%d Time %f"
                % (value, monotonic()) )




class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            print("my thread")
            # call a function




#