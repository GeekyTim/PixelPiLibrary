#!/usr/bin/env python3

import time

from pixelpi import PixelPi

"""
Available strip types (note, setting the white element of LEDs is currently not supported):

* `WS2812`
* `SK6812`
* `SK6812W`
* `SK6812_RGBW`
* `SK6812_RBGW`
* `SK6812_GRBW`
* `SK6812_GBRW`
* `SK6812_BRGW`
* `SK6812_BGRW`
* `WS2811_RGB`
* `WS2811_RBG`
* `WS2811_GRB`
* `WS2811_GBR`
* `WS2811_BRG`
* `WS2811_BGR`
"""

strip = PixelPi(2, 256, striptype='WS2812', brightness=40)
print(strip.getStripType)
print(strip.getLength)
print(strip.getStripPattern)
while True:
    print("Red")
    strip.setLED(255, 0, 0)
    strip.showStrip()
    print(strip.getStripPattern)
    time.sleep(1)

    print("Green")
    strip.setLED(0, 255, 0)
    strip.showStrip()
    print(strip.getStripPattern)
    time.sleep(1)

    print("Blue")
    strip.setLED(0, 0, 255)
    strip.showStrip()
    print(strip.getStripPattern)
    time.sleep(1)

    strip.clearStrip()
    strip.showStrip()
    print(strip.getStripPattern)

    for pixel in range(strip.getLength):
        # print("White: ", LED)
        strip.setLED(255, 255, 255, LED=pixel)
        strip.showStrip()
        print(strip.getStripPattern)
        time.sleep(0.25)
        strip.setLED(0, 0, 0, LED=pixel)
