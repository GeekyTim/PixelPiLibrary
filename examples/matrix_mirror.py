#!/usr/bin/env python3

import time

from pixelpi import Strip

strip = Strip(4, (8, 32), shape="zmatrix", ledtype='WS2812', brightness=30)

for x in range(int(strip.getWidth / 2)):
    for y in range(strip.getHeight):
        strip.setLEDs(led=(x, y), rgb=(128, 0, 0))
        strip.setLEDs(led=(strip.getWidth - 1 - x, y), rgb=(0, 0, 128))

strip.showLEDs()

try:
    while True:
        strip.mirror("horizontal")
        strip.showLEDs()
        time.sleep(0.2)

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
