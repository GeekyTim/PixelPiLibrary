#!/usr/bin/env python3

from pixelpi import PixelPi
import colorsys
import time

strip1 = PixelPi(1, 10, striptype='WS2812', brightness=0.2)
strip2 = PixelPi(2, 10, striptype='SK6812_GRBW', brightness=0.2)
strip3 = PixelPi(3, 10, striptype='WS2811_RGB', brightness=0.2)
strip4 = PixelPi(4, 10, striptype='WS2811_RGB', brightness=0.2)

spacing = 360.0 / 16.0
hue = 0

while True:
    hue = int(time.time() * 100) % 360
    for x in range(10):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        strip1.set_pixel(x, r, g, b)
        strip2.set_pixel(x, r, g, b)
        strip3.set_pixel(x, r, g, b)
        strip4.set_pixel(x, r, g, b)

    strip1.show()
    strip2.show()
    strip3.show()
    strip4.show()
    time.sleep(0.001)
