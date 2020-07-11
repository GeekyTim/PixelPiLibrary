#!/usr/bin/env python3

import colorsys
import time
from pixelpi import PixelPi

strip1 = PixelPi(1, 256, striptype='WS2812', brightness=0.2)
strip2 = PixelPi(2, 64, striptype='SK6812_GRBW', brightness=0.2)
strip3 = PixelPi(3, 288, striptype='WS2811_RGB', brightness=0.2)
strip4 = PixelPi(4, 300, striptype='WS2811_RGB', brightness=0.2)

#strip2.set_stripupdatestatus(False)
#strip3.set_stripupdatestatus(False)
#strip4.set_stripupdatestatus(False)

spacing = 360.0 / 16.0
hue = 0

while True:
    hue = int(time.time() * 100) % 360
    for x in range(strip1.length()):
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
