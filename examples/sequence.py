#!/usr/bin/env python3

from pixelpi import Strip

strip = Strip(2, 256, striptype='WS2812', brightness=40)

strip.clearStrip()
colourarray = strip.getLED()

print(colourarray)

for pixel in range(len(colourarray)):
    colourarray[pixel] = [pixel, 0, 255 - pixel, 51]

while True:
    strip.setLED(pattern=colourarray)
    strip.showStrip()
    # time.sleep(0.2)
    colourarray = strip.rotateStrip(colourarray, 1)
