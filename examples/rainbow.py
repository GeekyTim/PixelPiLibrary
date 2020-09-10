#!/usr/bin/env python3

import colorsys
import time

from pixelpi import Strip

# Change the terminal type to the type you have
strip1 = Strip(1, 180, ledtype='WS2811_GRB', brightness=50)
strip2 = Strip(2, 180, ledtype='WS2811_GRB', brightness=50)
strip3 = Strip(3, 180, ledtype='WS2811_GRB', brightness=50)
strip4 = Strip(4, 180, ledtype='WS2811_GRB', brightness=50)

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
