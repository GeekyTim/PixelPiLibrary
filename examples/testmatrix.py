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

strip = PixelPi(1, (8, 32), striptype='WS2812', stripshape="zmatrix", brightness=0.2)
print(strip.type)

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

    for y in range(strip.height):
        for x in range(strip.width):
            pixel = (x, y)
            strip.set_pixel(pixel, 255, 255, 255)
            strip.show()
            time.sleep(0.25)
            strip.set_pixel(pixel, 0, 0, 0)
            strip.show()
