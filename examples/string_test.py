#!/usr/bin/env python3

import time

from pixelpi import Strip

"""
Change the parameters below until you see the colours indicated on the screen:

    terminal = The screw terminal your LEDs are connected to
    
    size = The number of LEDs in your terminal (can be (x, y) for a matrix)
    
    shape = The 'shape' of the terminal.
            * `straight` - A led string (default)
            * `reverse` - A led string which starts at the opposite end
            * `matrix` - a normal matrix where the led order goes left to right. i.e:
              1 2 3 4
              5 6 7 8
              9 . . .
            * `zmatrix` - A matrix where the shift in the first row go left to right, the next one
              right to left. i.e:
              1 2 3 4
              8 7 6 5
              9 . . .
       
    ledtype = One of the supported terminal types:
          WS2812, SK6812, SK6812W, SK6812_RGBW, SK6812_RBGW, SK6812_GRBW, SK6812_GBRW, SK6812_BRGW,
          SK6812_BGRW, WS2811_RGB, WS2811_RBG, WS2811_GRB, WS2811_GBR, WS2811_BRG, WS2811_BGR

    brightness = The default brightness for all LEDs (0-255).   
"""

strip = Strip(terminal=1, size=256, shape='straight', ledtype='WS2812', brightness=40)

try:
    while True:
        print("Red")
        strip.setLEDs(rgb=(255, 0, 0))
        strip.showLEDs()
        time.sleep(1)

        print("Green")
        strip.setLEDs(rgb=(0, 255, 0))
        strip.showLEDs()
        time.sleep(1)

        print("Blue")
        strip.setLEDs(rgb=(0, 0, 255))
        strip.showLEDs()
        time.sleep(1)

        strip.clearLEDs()
        strip.showLEDs()

        for led in range(strip.getLength):
            print("White: ", led)
            strip.setLEDs(rgb=(255, 255, 255), led=led)
            strip.showLEDs()
            time.sleep(0.25)
            strip.setLEDs(rgb=(0, 0, 0), led=led)

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
