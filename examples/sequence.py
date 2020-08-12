#!/usr/bin/env python3
import colorsys
import numpy
import time
from pixelpi import PixelPi
from typing import Any

strip2 = PixelPi(2, 256, striptype='WS2812', brightness=40)

strip2.clearStrip()
colourarray = strip2.getStrip

print(colourarray)

for pixel in range(len(colourarray)):
    colourarray[pixel] = [pixel, 0, 255 - pixel, 51]

while True:
    strip2.sequence_set(colourarray)
    # strip2.sequence_reflect(colourarray)
    strip2.showStrip()
    # time.sleep(0.2)
    colourarray = strip2.sequence_rotate(colourarray, 1)
