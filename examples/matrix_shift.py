#!/usr/bin/env python3

from pixelpi import Strip
import time

strip = Strip(4, (8, 32), shape="zmatrix", ledtype='WS2812', brightness=30)

for x in range(strip.getWidth):
    strip.setLEDs(led=(x, 0), rgb=(128, 0, 0))

strip.showLEDs()

try:
    while True:
        strip.shift("up", 2)
        strip.showLEDs()
        time.sleep(0.2)

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
