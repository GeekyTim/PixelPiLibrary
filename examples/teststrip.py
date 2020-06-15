#!/usr/bin/env python3

from pixelpi import PixelPi
import time

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

strip = PixelPi(1, 20, striptype='WS2811_GRB', brightness=0.2)

while True:
    print("Red")
    strip.set_all(255, 0, 0)
    strip.show()
    time.sleep(1)

    print("Green")
    strip.set_all(0, 255, 0)
    strip.show()
    time.sleep(1)

    print("Blue")
    strip.set_all(0, 0, 255)
    strip.show()
    time.sleep(1)

    strip.clear()
    strip.show()

    for pixel in range(strip.get_striplength()):
        print("White: ", pixel)
        strip.set_pixel(pixel,255,255,255)
        strip.show()
        time.sleep(0.25)
        strip.set_pixel(pixel, 0, 0, 0)