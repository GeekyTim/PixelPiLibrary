#!/usr/bin/env python3

import colorsys
import time

from pixelpi import Strip, PixelPiButton


class MyButtons:
    def __init__(self, strips=None):
        self.__strips = strips

    def clear(self):
        try:
            print("clearing strips")
            if self.__strips is not None:
                for leds in self.__strips:
                    leds.clearLEDs()
                    leds.showLEDs()
        except:
            raise AttributeError('The strip list contained an error.')

    def whitelights(self):
        try:
            if self.__strips is not None:
                for strip in self.__strips:
                    strip.setLEDs(rgb=(255, 255, 255))
                    strip.showLEDs()
        except:
            raise AttributeError('The strip list contained an error.')


# Change the terminal type to the type you have
strip1 = Strip(1, 256, ledtype='WS2811_GRB', brightness=30)
strip2 = Strip(2, 256, ledtype='WS2811_GRB', brightness=30)
strip3 = Strip(3, 256, ledtype='WS2811_GRB', brightness=30)
strip4 = Strip(4, 256, ledtype='WS2811_GRB', brightness=30)

mybuttons = MyButtons([strip1, strip2, strip3, strip4])

button = PixelPiButton(callingclass=mybuttons, shortpress="clear", longpress="dosomethingelse")

spacing = 360.0 / 16.0
hue = 0

try:
    while True:
        hue = int(time.time() * 100) % 360
        for x in range(256):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]

            for strip in [strip1, strip2, strip3, strip4]:
                strip.setLEDs(rgb=(r, g, b), led=x)

        for strip in [strip1, strip2, strip3, strip4]:
            strip.showLEDs()

        time.sleep(0.001)

except KeyboardInterrupt:
    for strip in [strip1, strip2, strip3, strip4]:
        strip.clearLEDs()
        strip.showLEDs()
        del strip
