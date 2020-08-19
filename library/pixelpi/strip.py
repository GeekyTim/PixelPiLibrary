"""
.. module:: pixelpi
   :platform: Unix
   :synopsis: Control of WS281x LEDs with a Raspberry Pi
"""

from gpiozero import OutputDevice
from rpi_ws281x import PixelStrip, ws


class Strip:
    """
    Creates an led Strip with the provided configuration.

    :type terminal: int
    :param terminal:
        Which terminal the terminal is attached to (1-4).

    :type size: int or tuple
    :param size:
        The size of the LED string or matrix. Either the number of LEDs for a string, or (width, height) for a matrix.

    :type shape: str, optional
    :param shape:
        The 'shape' of the LEDs attached:

           * :data:`straight` - A LED string (default)
           * :data:`reverse` - A LED string which starts at the opposite end.
           * :data:`zmatrix` - A matrix where the LEDs in the first row go left to right, the next one
             right to left. i.e:

             | 1 2 3 4
             | 8 7 6 5
             | 9 . . .

           * :data:`matrix` - a normal matrix where the led order goes left to right. i.e:

             | 1 2 3 4
             | 5 6 7 8
             | 9 . . .

    :type ledtype: str
    :param ledtype:
        One of the supported LED types:

            ``WS2812`` *(default)*,
            ``SK6812``,
            ``SK6812W``,
            ``SK6812_RGBW``,
            ``SK6812_RBGW``,
            ``SK6812_GRBW``,
            ``SK6812_GBRW``,
            ``SK6812_BRGW``,
            ``SK6812_BGRW``,
            ``WS2811_RGB``,
            ``WS2811_RBG``,
            ``WS2811_GRB``,
            ``WS2811_GBR``,
            ``WS2811_BRG``,
            ``WS2811_BGR``

    :type brightness: int
    :param brightness: The default brightness for all LEDs (0-255).
    """

    ledtypeslist = ["WS2812", "SK6812", "SK6812W", "SK6812_RGBW", "SK6812_RBGW", "SK6812_GRBW", "SK6812_GBRW",
                    "SK6812_BRGW", "SK6812_BGRW", "WS2811_RGB", "WS2811_RBG", "WS2811_GRB", "WS2811_GBR",
                    "WS2811_BRG", "WS2811_BGR"]

    matrixshapelist = ["zmatrix", "matrix"]
    stringshapelist = ["straight", "reverse"]
    allshapeslist = matrixshapelist + stringshapelist

    rotatelist = ["LEFT", "RIGHT", "UP", "DOWN"]

    mirrorlist = ["HORIZONTAL", "VERTICAL"]

    def __init__(self, terminal, size, shape='straight', ledtype='WS2812', brightness=255):
        # ---------------------------------------------
        # Which terminal connection is being used (1 to 4)
        # ---------------------------------------------
        if terminal == 1:
            self.__controlpin = 10
            self.__channel = 0
            self.__onoffpin = 27
        elif terminal == 2:
            self.__controlpin = 12
            self.__channel = 0
            self.__onoffpin = 4
        elif terminal == 3:
            self.__controlpin = 21
            self.__channel = 0
            self.__onoffpin = 17
        elif terminal == 4:
            self.__controlpin = 13
            self.__channel = 1
            self.__onoffpin = 22
        else:
            raise ValueError('The terminal number must be between 1 and 4.')
        self.__stripnum = terminal

        # --------------
        # The terminal type
        # --------------
        if ledtype not in self.ledtypeslist:
            raise ValueError('This terminal type is not supported.')
        self.__striptype = ledtype

        supportedstriptypes = {}
        for t in ws.__dict__:
            if '_STRIP' in t:
                k = t.replace('_STRIP', '')
                v = getattr(ws, t)
                supportedstriptypes[k] = v
        self.__internalstriptype = supportedstriptypes[ledtype]

        # ---------------
        # The terminal shape
        # ---------------
        if shape not in self.allshapeslist:
            raise ValueError('The terminal shape is not supported.')
        elif shape in self.matrixshapelist and type(size) is not tuple:
            raise ValueError('A matrix shape has been defined, but the size is not a tuple (i.e. (x, y)).')
        elif shape not in self.matrixshapelist and type(size) is tuple:
            raise ValueError('A non-matrix shape has been defined, but the size is a tuple.')
        self.__stripshape = shape

        # -----------------------------------------
        # The size of the terminal
        # striplength is the total number of shift
        # -----------------------------------------
        if type(size) is tuple:
            if len(size) != 2:
                raise ValueError('The matrix shape must be defined in width and length size (x, y) only.')
            width, height = size
            striplength = height * width
            self.__width = width
            self.__height = height
        else:
            striplength = size
            self.__width = 1
            self.__height = striplength

        if striplength <= 0:
            raise ValueError('The terminal length needs to be 1 or more.')
        self.__striplength = striplength

        # -----------------------------------
        # The default brightness at the start
        # -----------------------------------
        self.__brightness = self.__checkBrightness(brightness)

        # -----------------------------------------------
        # A list to hold the led colours and brightness
        # -----------------------------------------------
        self.__pixels = [[0, 0, 0, self.__brightness]] * self.__striplength

        # ----------------------------
        # Set up the rpi_ws281x object
        # ----------------------------
        self.__strip = PixelStrip(self.__striplength, self.__controlpin, 800000, 10, False, self.__brightness,
                                  self.__channel, self.__internalstriptype)

        # ---------------------
        # Start the terminal logic
        # ---------------------
        self.__strip.begin()

        # -------------------------------------------------------------------
        # Set up the pin which defines whether the terminal is written to or not
        # -------------------------------------------------------------------
        self.__statuspin = OutputDevice(self.__onoffpin, active_high=False, initial_value=False)
        self.updateStatus = True

        # ---------------
        # Clear the terminal
        # ---------------
        self.clearLEDs()

    def __del__(self):
        """Disposes of the rpi_ws281x object"""
        del self.__strip

    @staticmethod
    def __version():
        return __version__

    @property
    def getLength(self):
        """Returns how many LEDs are in the strip/matrix."""
        return self.__striplength

    @property
    def getWidth(self):
        """Returns the width of the matrix (1 if an LED string)."""
        return self.__width

    @property
    def getHeight(self):
        """Returns the height of the matrix (or length of an LED string)."""
        return self.__height

    @property
    def getStripType(self):
        """Returns the set LED type."""
        return self.__striptype

    @property
    def getStripNumber(self):
        """Returns the terminal the LEDs are attached to."""
        return self.__stripnum

    @property
    def updateStatus(self):
        """
        Returns or sets whether output is currently enabled for the LEDs.

        When set to ``False``, the current LED pattern will remain unchanged even if the pattern is changed and
        :class:`showLEDs()` is called.

        :getter: Returns the status.
        :setter: Sets the status.
        :type: bool
        """
        return self.__statuspin.value == 1

    @updateStatus.setter
    def updateStatus(self, status=True):
        """
        The setter for updateStatus property.
        """
        if status:
            self.__statuspin.on()
        else:
            self.__statuspin.off()

    def __checkBrightness(self, brightness):
        """
        Checks whether the brightness value given is within range (0-255)

        :type brightness: int or None
        :param brightness:
            A value between 0 (off) and 255 (full brightness)
        """
        if brightness is None:
            brightness = self.__brightness
        else:
            if 0 < brightness > 255:
                raise ValueError('Brightness must be between 0 and 255')

        return brightness

    @staticmethod
    def __checkRGB(rgb):
        """Checks whether the rgb value passed in is valid."""
        if type(rgb) is not tuple:
            raise ValueError('The rgb value must be a tuple of the form (r, g, b).')
        elif len(rgb) != 3:
            raise ValueError('The rgb tuple must have three elements (r, g, b).')

        red, green, blue = [int(c) & 0xff for c in rgb]

        return red, green, blue

    @staticmethod
    def __checkPattern(pattern):
        """
        Checks whether the pattern passed in is valid

        :param pattern: A list of the RGB and brightness values of each led in the terminal
        """
        if len(pattern) == 0:
            raise ValueError("The pattern must have elements")
        if len(pattern[0]) != 4:
            raise ValueError("Each index of the pattern must have four elements (red, green, blue, brightness)")

        return pattern

    def __setBrightness(self, brightness, led=None):
        """
        Sets the brightness of one or more LEDs.

        :type brightness: int or None
        :param brightness: The brightness

        :type led: int or None
        :param led: If defined, only set that led, otherwise set all
        """
        brightness = self.__checkBrightness(brightness)

        if led is None:
            for led in range(self.__striplength):
                self.__pixels[led][3] = brightness
        else:
            pixelnumber = self.__translate(led)

            if 0 <= pixelnumber < self.__striplength:
                raise ValueError('The led index is out of range.')

            self.__pixels[led][3] = brightness

    def __setImage(self, image, position=None):
        """
        Plots an RGB image to the matrix or string of LEDs.

        :type image: RGB Format image
        :param image: An image in RGB format (see PILLOW library)

        :type position: int, tuple or None
        :param position: The location on the matrix
        """
        if image.mode != 'RGB':
            raise ValueError("The image must be in RGB format.")

        imagewidth, imageheight = image.size

        if self.__stripshape in self.matrixshapelist:
            if position is None:
                position = (0, 0)
            elif type(position) is not tuple:
                raise ValueError("A matrix shape has been defined, but the size is not a tuple (i.e. (x, y)).")
            elif len(position) != 2:
                raise ValueError(
                    'A matrix shape has been defined, but the start position does not have two elements (i.e. (x, y)).')
            px, py = position
            width = min(imagewidth, self.__width)
            height = min(imageheight, self.__height)
        else:
            if position is None:
                position = 0
            if type(position) is tuple:
                raise ValueError('A non-matrix shape has been defined, but the size is a tuple.')
            px, py = position, 0
            width = 1
            height = min(imageheight, self.__height)

        imagecolours = list(image.getdata())

        for y in range(height):
            for x in range(width):
                r, g, b = imagecolours[x + y * 8]
                self.setLEDs(led=(px + x, py + y), rgb=(r, g, b))

    def __setPattern(self, pattern):
        """
        Sets the RGB and brightness of the LEDs using the pattern passed in

        :param pattern:
        """
        pattern = self.__checkPattern(pattern)

        for pixelnumber in range(min(self.__striplength, len(pattern))):
            self.__pixels[pixelnumber] = pattern[pixelnumber]

    def __translate(self, pixel):
        """Translates co-ordinates for various different shapes"""

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

    def getLEDs(self, led=None):
        """
        If ``led`` is supplied, returns the RGB and brightness values of a specific LED.

        If led is not supplied or set to ``None`` a list of red, green, blue and brightness values for each LED
        is returned in a list.

        :type led: int, tuple or None
        :param led: The led location, either the LED count from the start, or the x,y matrix location,
            or if None, a list of all LEDs will be returned
        :return: (red, green, blue, brightness) or a list of (red, green, blue, brightness)
        """

        if led is None:
            return self.__pixels
        else:
            pixelnumber = self.__translate(led)

            if 0 <= pixelnumber < self.__striplength:
                r, g, b, brightness = self.__pixels[pixelnumber]
            else:
                r, g, b, brightness = [0, 0, 0, 0]

            return r, g, b, brightness

    def setLEDs(self, led=None, rgb=None, brightness=None, image=None, pattern=None):
        """
        Sets the RGB value, and optionally brightness, of one or more LEDs.

        If ``led`` is not supplied or set to ``None``, all LEDs will be set to the
        defined colour and brightness.

        If a matrix is being used, ``led`` can either be the LED count from the first LED,
        or the (x, y) location.

        If a brightness value is not supplied, or set to ``None``, the current LED brightness
        will be kept.

        If an image is supplied, then it must be in RGB format (see
        `Pillow image file formats <https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html>`_)

        If a pattern is supplied, it must be a list consisting of a tuple with four elements,
        ``(red, green, blue, brightness)``.

        :type led: int, tuple or None
        :param led: The LED location or None to set all LEDs to the desired colour.

        :type rgb: tuple or None
        :param rgb: A tuple consisting of 3 elements, (red, green, blue), with each value being between 0 and 255.

        :type brightness: int or None
        :param brightness: A value between 0 (dim) to 255 (very bright) or None to take the default.

        :type image: image or None
        :param image: An image object (see PIL or Pillow libraries) containing an RGB formatted image.

        :type pattern: list or None
        :param pattern: A list of the RGB and brightness values for each LED, in numerical order from the start of the
            strip/matrix.
        """

        if image is not None:
            self.__setImage(image, position=led)
        elif pattern is not None:
            self.__setPattern(pattern)
        elif led is None and rgb is None and brightness is None:
            self.clearLEDs()
        else:
            if rgb is None:
                self.__setBrightness(brightness, led)
            else:
                red, green, blue = self.__checkRGB(rgb)

                if led is None:
                    brightness = self.__checkBrightness(brightness)
                    self.__pixels = [[red, green, blue, brightness]] * self.__striplength
                else:
                    pixelnumber = self.__translate(led)

                    if 0 <= pixelnumber < self.__striplength:
                        if brightness is None:
                            brightness = self.__pixels[pixelnumber][3]

                        self.__pixels[pixelnumber] = [red, green, blue, brightness]

    def clearLEDs(self):
        """
        Clears the LEDs (sets them to black), leaving the brightness as it is.
        """
        for pixel in range(self.__striplength):
            self.__pixels[pixel][0:3] = [0, 0, 0]

    def shift(self, direction="UP", shift=1):
        """
        Shifts the LEDs on the matrix or string by :data:`shift` LEDs in the direction specified.

        :type direction: str
        :param direction: The direction the LEDs should shift (LEFT, RIGHT, UP, DOWN)

        :type shift: int
        :param shift: The number of LEDs the matrix/string should be moved in the specified direction.
        """
        direction = direction.upper()
        if direction not in self.rotatelist:
            raise ValueError('The rotation direction must be one of LEFT, RIGHT, UP or DOWN.')

        if self.__stripshape in self.stringshapelist:
            if self.__striplength < shift or shift <= 0:
                raise ValueError('The shift value must be positive and shorter than the string length.')

            if direction == "LEFT" or direction == "UP":
                for _ in range(shift):
                    self.__pixels.insert(0, self.__pixels[self.__striplength - 1])
                    self.__pixels.pop(self.__striplength)
            else:
                for _ in range(shift):
                    self.__pixels.append(self.__pixels[0])
                    self.__pixels.pop(0)
        else:
            if direction == "UP" or direction == "DOWN":
                if shift >= self.__height:
                    raise ValueError('The shift must be smaller than the height of the matrix.')

                if direction == "DOWN":
                    shift = -shift

                tempstrip = self.__pixels.copy()

                for y in range(self.__height):
                    newy = (y + shift) % self.__height
                    for x in range(self.__width):
                        self.__pixels[self.__translate((x, newy))] = tempstrip[self.__translate((x, y))]
            else:
                if shift >= self.__width:
                    raise ValueError('The shift must be smaller than the width of the matrix.')

                if direction == "LEFT":
                    shift = -shift

                tempstrip = self.__pixels.copy()

                for x in range(self.__width):
                    newx = (x + shift) % self.__width
                    for y in range(self.__height):
                        self.__pixels[self.__translate((newx, y))] = tempstrip[self.__translate((x, y))]

    def mirror(self, mirror="VERTICAL"):
        """
        Mirrors the matrix LEDs either in the :data:`VERTICAL` or :data:`HORIZONTAL` plane.

        Reverses the LED colours on an LED string. The ``mirror`` parameter is not required for strings.

        :type mirror: str
        :param mirror: :data:`VERTICAL` *(default)* or :data:`HORIZONTAL`
        """

        if self.__stripshape in self.matrixshapelist:
            mirror = mirror.upper()

            if mirror not in self.mirrorlist:
                raise ValueError('The mirror value must be either VERTICAL or HORIZONTAL.')

            tempstrip = self.__pixels.copy()

            if mirror == "VERTICAL":
                for y in range(int(self.__height / 2)):
                    for x in range(self.__width):
                        self.__pixels[self.__translate((x, y))] = tempstrip[
                            self.__translate((x, self.__height - 1 - y))]
                        self.__pixels[self.__translate((x, self.__height - 1 - y))] = tempstrip[
                            self.__translate((x, y))]
            else:
                for x in range(int(self.__width / 2)):
                    for y in range(self.__height):
                        self.__pixels[self.__translate((x, y))] = tempstrip[
                            self.__translate((self.__width - 1 - x, y))]
                        self.__pixels[self.__translate((self.__width - 1 - x, y))] = tempstrip[
                            self.__translate((x, y))]
        else:
            self.__pixels.reverse()

    def showLEDs(self):
        """
        Once you have set the colours of the string/matrix LEDs, use :class:`showLEDs` to update the LEDs.
        """
        for pixel in range(self.__strip.numPixels()):
            r, g, b, brightness = self.__pixels[pixel]
            self.__strip.setPixelColorRGB(pixel, r, g, b)
        self.__strip.show()
