#!/usr/bin/env python3

import time

from pixelpi import Strip

strip = Strip(1, 264, ledtype='WS2812', brightness=40)

strip.clearLEDs()
pattern = strip.getLEDs()

for pixel in range(int(len(pattern) / 2)):
    pattern[pixel] = [255, 0, 0, pattern[pixel][3]]
    pattern[strip.getLength - pixel-1] = [0, 0, 255, pattern[strip.getLength - pixel-1][3]]

strip.setLEDs(pattern=pattern)

try:
    while True:
        strip.mirror()
        strip.showLEDs()
        time.sleep(1)

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
