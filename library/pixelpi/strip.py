"""
.. module:: pixelpi
   :platform: Unix
   :synopsis: Control of WS281x LEDs with a Raspberry Pi
"""

__version__ = '0.1.1'

import atexit

from gpiozero import OutputDevice
from rpi_ws281x import PixelStrip, ws


class Strip:
    """
    Creates an LED Strip with the provided configuration.

    :type strip: int
    :param strip:
        Which terminal the strip is attached to (1-4).

    :type stripsize: int
    :param stripsize:
        The size of the strip - either length for a string, or (width, height) for matrices.

    :type stripshape: str, optional
    :param stripshape:
        The 'shape' of the strip.

                       * :data:`straight` - A LED string (default)
                       * :data:`reverse` - A LED string which starts at the opposite end
                       * :data:`zmatrix` - A matrix where the pixels in the first row go left to right, the next one
                         right to left. i.e:
                         | 1 2 3 4
                         | 8 7 6 5
                         | 9 . . .
                       * :data:`matrix` - a normal matrix where the LED order goes left to right. i.e:
                         | 1 2 3 4
                         | 5 6 7 8
                         | 9 . . .

    :type striptype: str
    :param striptype:
        One of the supported strip types:

                      WS2812, SK6812, SK6812W, SK6812_RGBW, SK6812_RBGW, SK6812_GRBW, SK6812_GBRW, SK6812_BRGW,
                      SK6812_BGRW, WS2811_RGB, WS2811_RBG, WS2811_GRB, WS2811_GBR, WS2811_BRG, WS2811_BGR

    :type brighness: int
    :param brightness:
        The default brightness for all pixels (0-255).
    """

    striptypes = ["WS2812", "SK6812", "SK6812W", "SK6812_RGBW", "SK6812_RBGW", "SK6812_GRBW", "SK6812_GBRW",
                  "SK6812_BRGW", "SK6812_BGRW", "WS2811_RGB", "WS2811_RBG", "WS2811_GRB", "WS2811_GBR",
                  "WS2811_BRG", "WS2811_BGR"]
    stripshapes = ["straight", "zmatrix", "matrix", "reverse"]
    stripmatrixshapes = ["zmatrix", "matrix"]
    stripstringshapes = ["straight", "reverse"]

    ROTATE_LIST = ["LEFT", "RIGHT", "UP", "DOWN"]

    def __init__(self, strip, stripsize, stripshape='straight', striptype='WS2812', brightness=255):
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
        self.__checkBrightness(brightness)
        self.__brightness = brightness

        # -----------------------------------------------
        # A list to hold the LED colours and brightness
        # -----------------------------------------------
        self.__pixels = [[0, 0, 0, self.__brightness]] * self.__striplength

        # ----------------------------
        # Set up the rpi_ws281x object
        # ----------------------------
        self.__strip = PixelStrip(self.__striplength, self.__controlpin, 800000, 10, False, self.__brightness,
                                  self.__channel, self.__internalstriptype)

        # ---------------------
        # Start the strip logic
        # ---------------------
        self.__strip.begin()

        # -------------------------------
        # Always clear the pixels on exit
        # -------------------------------
        atexit.register(self.__atexit)

        # -------------------------------------------------------------------
        # Set up the pin which defines whether the strip is written to or not
        # -------------------------------------------------------------------
        self.__statuspin = OutputDevice(self.__onoffpin, active_high=False, initial_value=False)
        self.updateStatus = True

        # ---------------
        # Clear the strip
        # ---------------
        self.clearStrip()

    @property
    def getLength(self):
        """Returns how many LEDs are in the strip."""
        return self.__striplength

    @property
    def getWidth(self):
        """Returns the width of the matrix."""
        return self.__width

    @property
    def getHeight(self):
        """Returns the height of the matrix."""
        return self.__height

    @property
    def getStripType(self):
        """Returns the strip LED type."""
        return self.__striptype

    @property
    def getStripNumber(self):
        """Returns terminal the strip is attached to."""
        return self.__strip

    @property
    def getStripPattern(self):
        """Returns the RGB and brightness of each LED in the strip as a list."""
        return self.__pixels

    @property
    def getUpdateStatus(self):
        """
        Returns whether output is currently enabled for the strip.

        See setUpdateStatus() method.
        """
        return self.__statuspin.value == 1

    def setUpdateStatus(self, status=True):
        """
        Sets whether the strip output is to be used. When turned off, the current LED pattern will remain.

        :type status: bool
        :param status:
            On when :data:`True`, Off when :data:`False`
        """
        if status:
            self.__statuspin.on()
        else:
            self.__statuspin.off()

    @staticmethod
    def __checkBrightness(brightness):
        """
        Checks whether the brightness value given is within range (0-255)

        :type brightness: int
        :param brightness:
            A value between 0 (off) and 255 (full brightness)
        """
        if brightness is not None:
            if 0 < brightness > 255:
                raise ValueError("Brightness must be between 0 and 255")

    def setBrightness(self, brightness, pixel=None):
        """
        Sets the brightness of one or more LEDs in the strip.

        :param brightness: 0 to 255
        :param pixel: If defined, only set that LED, otherwise set all
        """
        self.__checkBrightness(brightness)

        if pixel is None:
            for pixel in range(self.__striplength):
                self.__pixels[pixel][3] = brightness
        else:
            pixelnumber = self.__translate(pixel)

            if 0 <= pixelnumber < self.__striplength:
                raise ValueError('The LED index is out of range.')

            self.__pixels[pixel][3] = brightness

    def getLED(self, pixel):
        """
        Gets the RGB and brightness value of a specific LED.

        :param pixel: the LED location, either the LED count from the start, or the x,y matrix location
        :return: r, g, b, brightness
        """
        pixelnumber = self.__translate(pixel)

        if 0 <= pixelnumber < self.__striplength:
            r, g, b, brightness = self.__pixels[pixelnumber]
        else:
            r, g, b, brightness = [0, 0, 0, 0]

        return r, g, b, brightness

    def setLED(self, r, g, b, LED=None, brightness=None):
        """
        Sets the RGB value, and optionally brightness, of one or more LEDs.

        If you don't define the LED, all LEDs will be set the defined colour.

        If you are using a matrix, you can use either the LED count from the start, or the (x, y) location

        If you don't supply a brightness value, the current LED brightness will be kept.

        :param r: Red: 0 to 255
        :param g:  Green: 0 to 255
        :param b:  Blue: 0 to 255
        :param brightness:  Brightness: 0 to 255 or None to take the default
        :param LED: The pixel location or None to set all
        """
        self.__checkBrightness(brightness)

        if LED is None:
            if brightness is None:
                brightness = self.__brightness

            self.__pixels = [[r, g, b, brightness]] * self.__striplength
        else:
            pixelnumber = self.__translate(LED)

            if 0 <= pixelnumber < self.__striplength:
                if brightness is None:
                    brightness = self.__pixels[pixelnumber][3]

                self.__pixels[pixelnumber] = [r, g, b, brightness]

    def setImage(self, image, position=(0, 0)):
        """
        Plots an RGB image to the strip (or matrix)

        :param image: An image in RGB format (see PILLOW library)
        :param position: The location on the strip
        """
        if image.mode != 'RGB':
            raise ValueError("The image must be in RGB format.")

        imagewidth, imageheight = image.size

        if self.__stripshape in self.stripmatrixshapes:
            if type(position) is not tuple:
                raise ValueError("A matrix shape has been defined, but the size is not a tuple (i.e. (x, y)).")
            px, py = position
            width = min(imagewidth, self.__width)
            height = min(imageheight, self.__height)
        else:
            if type(position) is tuple:
                raise ValueError("A non-matrix shape has been defined, but the size is a tuple.")
            px, py = position, 1
            width = 1
            height = min(imageheight, self.__height)

        pixel_values = list(image.getdata())

        for y in range(height):
            for x in range(width):
                r, g, b = pixel_values[x + y * 8]
                self.setLED((px + x, py + y), r, g, b)

    @staticmethod
    def __checkStrip(pattern):
        """
        Checks whether the pattern passed in is valid

        :param pattern: A list of the RGB and brighness values of each LED in the strip
        """
        if len(pattern) == 0:
            raise ValueError("The sequence must have elements")
        if len(pattern[0]) != 4:
            raise ValueError("Each element of the sequence must have four elements (r, g, b, brightness)")

    def setStripPattern(self, pattern):
        """
        Sets the RGB and brightness of the strip using the pattern passed in

        :param pattern:
        """
        self.__checkStrip(pattern)

        for pixelnumber in range(min(self.__striplength, len(pattern))):
            self.__pixels[pixelnumber] = pattern[pixelnumber]

    def rotateStrip(self, direction, pixels):
        """
        Rotates the pixels on the strip

        :param direction: The direction the strip should rotate (LEFT, RIGHT, UP, DOWN)
        :param pixels: The number of pixels the strip should rotate
        """
        direction = direction.upper()
        if direction not in self.ROTATE_LIST:
            raise ValueError("The rotation direction must be one of LEFT, RIGHT, UP or DOWN.")

        if self.__stripshape in self.stripstringshapes:
            if self.__striplength < pixels or pixels <= 0:
                raise ValueError("The pixels value must be positive and shorter than the strip length.")

            if direction == "LEFT" or direction == "UP":
                for _ in range(pixels):
                    self.__pixels.insert(0, self.__pixels[self.__striplength - 1])
                    self.__pixels.pop(self.__striplength)
            else:
                for _ in range(pixels):
                    self.__pixels.append(self.__pixels[0])
                    self.__pixels.pop(0)

    def reflectStrip(self, mirror="VERTICAL"):
        """
        Reflects the strip

        :param mirror: Use mirror for matrices to indicate whether they should be reflected in the vertical or
                       horizontal axis
        """
        if self.__stripshape in self.stripmatrixshapes:
            _ = 0
        else:
            self.__pixels.reverse()

    def clearStrip(self):
        """
        Clears the LED buffer, leaving the brighness as is
        """
        for pixel in range(self.__striplength):
            self.__pixels[pixel][0:3] = [0, 0, 0]

    def showStrip(self):
        """
        Once you have set the colours of the strip/matrix LEDs, use this method to output to the strip to the LEDs.
        """
        for pixel in range(self.__strip.numPixels()):
            r, g, b, brightness = self.__pixels[pixel]
            self.__strip.setPixelColorRGB(pixel, r, g, b)
        self.__strip.show()

    def __translate(self, pixel):
        """Translates matrix co-ordinates for various different shapes"""

        realpixel = -1
        if self.__stripshape == "straight" or type(pixel) is not tuple:
            if 0 <= pixel < self.__striplength:
                realpixel = pixel
        elif self.__stripshape == "reverse":
            if 0 <= pixel < self.__striplength:
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

    def __atexit(self):
        """This will be called when the program exits to clear the LEDs"""
        self.clearStrip()
        self.showStrip()
