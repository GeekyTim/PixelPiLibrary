from time import sleep

from PIL import Image
from pixelpi import Strip

im = Image.open("image.png").convert(mode='RGB', colors=256)

# strip1 = Strip(2, (8, 8), ledtype='SK6812_GRBW', shape="matrix", brightness=0.2)
strip = Strip(terminal=4, size=(8, 32), ledtype='WS2812', shape="zmatrix", brightness=30)

try:
    i = 0
    while True:
        i = i + 1
        if i >= 32:
            i = 0

        for r in range(4):
            im = im.transpose(Image.ROTATE_90)
            strip.setLEDs(led=(0, i), image=im)
            strip.showLEDs()
            sleep(0.5)

        strip.clearLEDs()
        strip.showLEDs()

except KeyboardInterrupt:
    strip.clearLEDs()
    strip.showLEDs()
    del strip
