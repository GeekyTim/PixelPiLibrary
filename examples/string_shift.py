#!/usr/bin/env python3

from pixelpi import Strip

strip = Strip(1, 256, ledtype='WS2812', brightness=40)

strip.clearLEDs()
pattern = strip.getLEDs()

for pixel in range(len(pattern)):
    pattern[pixel] = [0, pixel, 0, pattern[pixel][3]]

strip.setLEDs(pattern=pattern)

try:
    while True:
        strip.showLEDs()
        strip.shift("down", 2)

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
