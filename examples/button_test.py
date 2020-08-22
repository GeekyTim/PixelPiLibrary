from pixelpi import PixelPiButton
from signal import pause
import gc

def dosomething():
    print("Done something")

button = PixelPiButton(shortpress=dosomething())

pause()
