from PIL import Image
from pixelpi import PixelPi
from time import sleep

im = Image.open("image.png").convert(mode='RGB', colors=256)

# strip1 = PixelPi(2, (8, 8), striptype='SK6812_GRBW', stripshape="matrix", brightness=0.2)
strip2 = PixelPi(2, (8, 32), striptype='WS2812', stripshape="zmatrix", brightness=0.2)

i = 0
while True:
    i = i + 1
    if i >= 32:
        i = 0
    im = im.transpose(Image.ROTATE_90)
    #    strip1.set_image(im)
    strip2.set_image(im, (0, i))
    strip2.show()
    sleep(0.5)
    im = im.transpose(Image.ROTATE_90)
    #    strip1.set_image(im)
    strip2.set_image(im, (0, i))
    strip2.show()
    sleep(0.5)
    im = im.transpose(Image.ROTATE_90)
    #    strip1.set_image(im)
    strip2.set_image(im, (0, i))
    strip2.show()
    sleep(0.5)
    im = im.transpose(Image.ROTATE_90)
    #    strip1.set_image(im)
    strip2.set_image(im, (0, i))
    strip2.show()
    sleep(0.5)
    strip2.clear()
    strip2.show()
