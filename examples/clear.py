#!/usr/bin/env python3

from pixelpi import Strip

strip1 = Strip(1, 300, brightness=40)
strip2 = Strip(2, 300, brightness=40)
strip3 = Strip(3, 300, brightness=40)
strip4 = Strip(4, 300, brightness=40)

for strip in [strip1, strip2, strip3, strip4]:
    strip.clearStrip()
    strip.showStrip()
    del strip
