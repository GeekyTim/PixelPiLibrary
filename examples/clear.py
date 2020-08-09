#!/usr/bin/env python3

import colorsys
import time
from pixelpi import PixelPi

"""
Available strip types (note, setting the white element of LEDs is currently not supported):

* `WS2812`
* `SK6812`
* `SK6812W`
* `SK6812_RGBW`
* `SK6812_RBGW`
* `SK6812_GRBW`
* `SK6812_GBRW`
* `SK6812_BRGW`
* `SK6812_BGRW`
* `WS2811_RGB`
* `WS2811_RBG`
* `WS2811_GRB`
* `WS2811_GBR`
* `WS2811_BRG`
* `WS2811_BGR`
"""

strip = PixelPi(1, 300, striptype='WS2811_GRB', brightness=0.2)
strip = PixelPi(2, 300, striptype='WS2811_GRB', brightness=0.2)
strip = PixelPi(3, 300, striptype='WS2811_GRB', brightness=0.2)
strip = PixelPi(4, 300, striptype='WS2811_GRB', brightness=0.2)

strip.clear()
strip.show()
