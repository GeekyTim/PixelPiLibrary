__version__ = '0.0.4'

import atexit
from PIL import Image
from gpiozero import Button, OutputDevice
from rpi_ws281x import PixelStrip, ws

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


class PixelPi:
    striptypes = ["WS2812", "SK6812", "SK6812W", "SK6812_RGBW", "SK6812_RBGW", "SK6812_GRBW", "SK6812_GBRW",
                  "SK6812_BRGW", "SK6812_BGRW", "WS2811_RGB", "WS2811_RBG", "WS2811_GRB", "WS2811_GBR",
                  "WS2811_BRG", "WS2811_BGR"]
    stripshapes = ["straight", "zmatrix", "matrix", "reverse"]
    stripmatrixshapes = ["zmatrix", "matrix"]

    def __init__(self, strip, stripsize, stripshape='straight', striptype='WS2812', brightness=1.0):
        """Initialise the LED Strip using the details given"""

        # ---------------------------------------------
        # Which strip connection is being used (1 to 4)
        # ---------------------------------------------
        if strip == 1:
            self.__controlpin = 10
            self.__channel = 0
            self.__onoffpin = 27
        elif strip == 2:
            self.__controlpin = 12
            self.__channel = 0
            self.__onoffpin = 4
        elif strip == 3:
            self.__controlpin = 21
            self.__channel = 0
            self.__onoffpin = 17
        elif strip == 4:
            self.__controlpin = 13
            self.__channel = 1
            self.__onoffpin = 22
        else:
            raise ValueError("The strip number must be between 1 and 4.")
        self.__strip = strip

        # --------------
        # The strip type
        # --------------
        if striptype not in self.striptypes:
            raise ValueError("This strip type is not supported.")
        self.__striptype = striptype

        supportedstriptypes = {}
        for t in ws.__dict__:
            if '_STRIP' in t:
                k = t.replace('_STRIP', '')
                v = getattr(ws, t)
                supportedstriptypes[k] = v
        self.__internalstriptype = supportedstriptypes[striptype]

        # ---------------
        # The strip shape
        # ---------------
        if stripshape not in self.stripshapes:
            raise ValueError("The strip shape is not supported.")
        elif stripshape in self.stripmatrixshapes and type(stripsize) is not tuple:
            raise ValueError("A matrix shape has been defined, but the size is not a tuple (i.e. (x, y)).")
        elif stripshape not in self.stripmatrixshapes and type(stripsize) is tuple:
            raise ValueError("A non-matrix shape has been defined, but the size is a tuple.")
        self.__stripshape = stripshape

        # -----------------------------------------
        # The size of the strip
        # striplength is the total number of pixels
        # -----------------------------------------
        if type(stripsize) is tuple:
            if len(stripsize) != 2:
                raise ValueError("The matrix shape must be defined in width and length size (x, y) only.")
            width, height = stripsize
            striplength = height * width
            self.__width = width
            self.__height = height
        else:
            striplength = stripsize
            self.__width = 1
            self.__height = striplength

        if striplength <= 0:
            raise ValueError("The strip length needs to be 1 or more.")
        self.__striplength = striplength

        # -----------------------------------
        # The default brightness at the start
        # -----------------------------------
        if brightness < 0 or brightness > 1.0:
            raise ValueError("The brightness must be between 0.0 and 1.0")
        self.__brightness = int(brightness * 255)

        # -------------------------------------------------
        # An array to hold the pixel colours and brightness
        # -------------------------------------------------
        self.__pixels = [[0, 0, 0, self.__brightness]] * self.__striplength

        # ---------------------------
        # Set up the rpi_ws281x strip
        # ---------------------------
        self.__strip = PixelStrip(self.__striplength, self.__controlpin, 800000, 10, False, self.__brightness,
                                  self.__channel, self.__internalstriptype)

        # ---------------------
        # Start the strip logic
        # ---------------------
        self.__strip.begin()

        # -------------------------------
        # Always clear the pixels on exit
        # -------------------------------
        atexit.register(self.atexit)

        # -------------------------------------------------------------------
        # Set up the pin which defines whether the strip is written to or not
        # -------------------------------------------------------------------
        self.__statuspin = OutputDevice(self.__onoffpin, active_high=False, initial_value=False)
        self.updatestatus = True

        # ---------------
        # Clear the strip
        # ---------------
        self.clear()

    @property
    def length(self):
        """Gets how many LEDs are in the strip"""
        return self.__striplength

    @property
    def width(self):
        """Returns the width of the matrix"""
        return self.__width

    @property
    def height(self):
        """Returns the height of the matrix"""
        return self.__height

    @property
    def type(self):
        """Gets the strip type"""
        return self.__striptype

    @property
    def number(self):
        """Gets which output the strip is attached to"""
        return self.__strip

    @property
    def updatestatus(self):
        """Gets whether output is currently enabled for the strip"""
        return self.__statuspin.value == 1

    @updatestatus.setter
    def updatestatus(self, status=True):
        """Sets whether the strip output is to be used

        status: On when True, Off when False
        """
        if status:
            self.__statuspin.on()
        else:
            self.__statuspin.off()

    def set_brightness_all(self, brightness):
        """Set the brightness of all pixels in the strip.

        brightness: Brightness: 0.0 to 1.0
        """
        if brightness < 0 or brightness > 1:
            raise ValueError('Brightness should be between 0.0 and 1.0')

        for pixel in range(self.__striplength):
            self.__pixels[pixel][3] = int(brightness * 255)

    def set_brightness_pixel(self, pixel, brightness):
        """Set the brightness of all pixels.

        pixel: The pixel number in the strip
        brightness: Brightness: 0.0 to 1.0
        """
        pixelnumber = self.__translate(pixel)

        if 0 <= pixelnumber < self.__striplength:
            raise ValueError('The pixel index is out of range.')

        if brightness < 0 or brightness > 1:
            raise ValueError('Brightness should be between 0.0 and 1.0')

        self.__pixels[pixel][3] = int(brightness * 255)

    @property
    def get_pixel(self, pixel):
        """Gets the RGB and brightness value of a specific pixel."""
        pixelnumber = self.__translate(pixel)

        if 0 <= pixelnumber < self.__striplength:
            r, g, b, brightness = self.__pixels[pixelnumber]
        else:
            r, g, b, brightness = [0, 0, 0, 0]

        return r, g, b, brightness

    def set_pixel(self, pixel, r, g, b, brightness=None):
        """Set the RGB value, and optionally brightness, of a single pixel.

        If you don't supply a brightness value, the last value will be kept.

        pixel: The pixel position in the strip
        r: Red: 0 to 255
        g: Green: 0 to 255
        b: Blue: 0 to 255
        brightness: Brightness: 0.0 to 1.0
        """
        pixelnumber = self.__translate(pixel)

        if 0 <= pixelnumber < self.__striplength:
            r, g, b = [int(c) & 0xff for c in (r, g, b)]

            if brightness is None:
                brightness = self.__pixels[pixelnumber][3]

            self.__pixels[pixelnumber] = [r, g, b, brightness]

    def __fast_set_pixel(self, pixel, r, g, b, brightness=None):
        """Does not use the translate pixel"""
        if 0 <= pixel < self.__striplength:
            r, g, b = [int(c) & 0xff for c in (r, g, b)]

            if brightness is None:
                brightness = self.__pixels[self.__translate(pixel)][3]

            self.__pixels[pixel] = [r, g, b, brightness]

    def set_all(self, r, g, b, brightness=None):
        """Set the RGB value and optionally brightness of all pixels in the strip.

        If you don't supply a brightness value, the last value set for each pixel be kept.

        r: Amount of red: 0 to 255
        g: Amount of green: 0 to 255
        b: Amount of blue: 0 to 255
        brightness: Brightness: 0.0 to 1.0
        """
        for pixel in range(self.__striplength):
            self.__fast_set_pixel(pixel, r, g, b, brightness)

    def set_image(self, image, position=(0, 0)):
        if image.mode != 'RGB':
            raise ValueError("The image must be in RGB format.")

        px, py = position

        imagewidth, imageheight = image.size
        width = min(imagewidth, self.width)
        height = min(imageheight, self.height)

        pixel_values = list(image.getdata())

        for y in range(height):
            for x in range(width):
                r, g, b = pixel_values[x + y * 8]
                self.set_pixel((px + x, py + y), r, g, b)
        self.show()

    def clear(self):
        """Clear the pixel buffer."""
        for pixel in range(self.__striplength):
            self.__pixels[pixel][0:3] = [0, 0, 0]

    def show(self):
        """Output to the strip."""
        for pixel in range(self.__strip.numPixels()):
            r, g, b, brightness = self.__pixels[pixel]
            self.__strip.setPixelColorRGB(pixel, r, g, b)
        self.__strip.show()

    def __translate(self, pixel):
        """Translates matrix co-ordinates for various different shapes"""

        realpixel = -1
        if self.__stripshape == "straight" or type(pixel) is not tuple:
            if 0 <= pixel < self.__length:
                realpixel = pixel
        elif self.__stripshape == "reverse":
            if 0 <= pixel < self.__length:
                realpixel = self.__striplength - pixel
        elif self.__stripshape == "zmatrix":
            x, y = pixel
            if 0 <= x < self.__width and 0 <= y <= self.__height:
                if y % 2 == 0:
                    realpixel = (y * self.__width) + x
                else:
                    realpixel = ((y + 1) * self.__width) - (x + 1)
        elif self.__stripshape == "matrix":
            x, y = pixel
            if 0 <= x < self.__width and 0 <= y <= self.__height:
                realpixel = y * self.__width + x
        return realpixel

    def atexit(self):
        """This will be called when the program exits"""
        self.clear()
        self.show()
