#!/usr/bin/env python3

from pixelpi import Strip

strip1 = Strip(1, 180, ledtype='WS2811_GRB', brightness=50)
strip2 = Strip(2, 180, ledtype='WS2811_GRB', brightness=50)
strip3 = Strip(3, 180, ledtype='WS2811_GRB', brightness=50)
strip4 = Strip(4, 180, ledtype='WS2811_GRB', brightness=50)

strip1.clearLEDs()
pattern = strip1.getLEDs()

for pixel in range(len(pattern)):
    pattern[pixel] = [0, pixel, 0, pattern[pixel][3]]

for strip in [strip1, strip2, strip3, strip4]:
    strip.setLEDs(pattern=pattern)

try:
    while True:
        for strip in [strip1, strip2, strip3, strip4]:
            strip.showLEDs()
            strip.shift("down", 1)

except KeyboardInterrupt:
    for strip in [strip1, strip2, strip3, strip4]:
        strip.clearLEDs()
        strip.showLEDs()
        del strip
