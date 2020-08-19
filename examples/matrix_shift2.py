#!/usr/bin/env python3

from pixelpi import Strip
import time

strip = Strip(4, (8, 32), shape="zmatrix", ledtype='WS2812', brightness=30)

for y in range(strip.getHeight):
    strip.setLEDs(led=(0, y), rgb=(0, 0, 128))

strip.showLEDs()

try:
    while True:
        strip.shift("right", 1)
        strip.showLEDs()
        time.sleep(0.2)

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
