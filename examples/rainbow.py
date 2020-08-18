#!/usr/bin/env python3

import time

import colorsys
from pixelpi import Strip

strip1 = Strip(2, 300, stripshape='straight', striptype='WS2811_GRB', brightness=50)
# strip2 = Strip(2, 10, striptype='SK6812_GRBW', brightness=50)
# strip3 = Strip(3, 10, striptype='WS2811_RGB', brightness=50)
# strip4 = Strip(4, 10, striptype='WS2811_RGB', brightness=50)

spacing = 360.0 / 16.0
hue = 0

while True:
    hue = int(time.time() * 100) % 360
    for x in range(256):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        strip1.setLED(r, g, b, LED=x)
        # strip2.setLED(x, r, g, b)
        # strip3.setLED(x, r, g, b)
        # strip4.setLED(x, r, g, b)

    strip1.showStrip()
    # strip2.showStrip()
    # strip3.showStrip()
    # strip4.showStrip()
    time.sleep(0.001)
