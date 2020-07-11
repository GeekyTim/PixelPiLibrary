__version__ = '0.0.4'

import atexit
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
    def __init__(self, strip, stripsize, stripshape='straight', striptype='WS2812', brightness=1.0):
        """Initialise the LED Strip using the details given"""

        # Which strip connection is being used (1 to 4)
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

        # The strip types available
        striptypes = ["WS2812", "SK6812", "SK6812W", "SK6812_RGBW", "SK6812_RBGW", "SK6812_GRBW", "SK6812_GBRW",
                      "SK6812_BRGW", "SK6812_BGRW", "WS2811_RGB", "WS2811_RBG", "WS2811_GRB", "WS2811_GBR",
                      "WS2811_BRG", "WS2811_BGR"]
        if striptype not in striptypes:
            raise ValueError(
                "This strip type is not supported. Use one of WS2812, SK6812, SK6812W, SK6812_RGBW, SK6812_RBGW, "
                "SK6812_GRBW, SK6812_GBRW, SK6812_BRGW, SK6812_BGRW, WS2811_RGB, WS2811_RBG, WS2811_GRB, WS2811_GBR, "
                "WS2811_BRG, WS2811_BGR.")

        supportedstriptypes = {}
        for t in ws.__dict__:
            if '_STRIP' in t:
                k = t.replace('_STRIP', '')
                v = getattr(ws, t)
                supportedstriptypes[k] = v

        self.__stripshape = stripshape
        self.__striptype = supportedstriptypes[striptype]

        if type(stripsize) is tuple:
            length, width = stripsize
            striplength = length * width
        else:
            striplength = stripsize

        if striplength <= 0:
            raise ValueError("The strip length needs to be 1 or more.")
        self.__striplength = striplength

        if brightness < 0 or brightness > 1.0:
            raise ValueError("The brightness must be between 0.0 and 1.0")
        self.__brightness = int(brightness * 255)

        # Create an array to hold the pixel colours and brightness
        self.__pixels = [[0, 0, 0, self.__brightness]] * self.__striplength

        self.__strip = PixelStrip(self.__striplength, self.__controlpin, 800000, 10, False, self.__brightness,
                                  self.__channel, self.__striptype)
        self.__strip.begin()

        self.__clear_on_exit = True

        self.__statuspin = OutputDevice(self.__onoffpin, active_high=False, initial_value=False)
        self.updatestatus = True

        self.clear()

        atexit.register(self.atexit)

    @property
    def length(self):
        """Gets how many LEDs are in the strip"""
        return self.__striplength

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

    @property
    def clearonexit(self):
        return self.__clear_on_exit

    @clearonexit.setter
    def clearonexit(self, status=True):
        """Set if the pixel strip should be cleared upon program exit."""
        self.__clear_on_exit = status

    def set_brightness_all(self, brightness):
        """Set the brightness of all pixels in the strip.

        brightness: Brightness: 0.0 to 1.0
        """
        if brightness < 0 or brightness > 1:
            raise ValueError('Brightness should be between 0.0 and 1.0')

        for pixel in range(self.__striplength):
            self.__pixels[pixel][3] = brightness

    def set_brightness_pixel(self, pixel, brightness):
        """Set the brightness of all pixels.

        pixel: The pixel number in the strip
        brightness: Brightness: 0.0 to 1.0
        """

        if pixel < 0 or pixel > self.__striplength:
            raise ValueError('The pixel index is out of range.')

        if brightness < 0 or brightness > 1:
            raise ValueError('Brightness should be between 0.0 and 1.0')

        self.__pixels[pixel][3] = brightness

    @property
    def get_pixel(self, lednum):
        """Gets the RGB and brightness value of a specific pixel."""
        if lednum > 0 and lednum < self.__striplength:
            r, g, b, brightness = self.__pixels[lednum]
        else:
            r, g, b, brightness = [0, 0, 0, 0]

        return r, g, b, brightness

    def set_pixel(self, lednum, r, g, b, brightness=None):
        """Set the RGB value, and optionally brightness, of a single pixel.

        If you don't supply a brightness value, the last value will be kept.

        pixel: The pixel position in the strip
        r: Red: 0 to 255
        g: Green: 0 to 255
        b: Blue: 0 to 255
        brightness: Brightness: 0.0 to 1.0
        """
        if 0 <= lednum < self.__striplength:
            r, g, b = [int(c) & 0xff for c in (r, g, b)]

            if brightness is None:
                brightness = self.__pixels[lednum][3]

            self.__pixels[lednum] = [r, g, b, brightness]

    def set_all(self, r, g, b, brightness=None):
        """Set the RGB value and optionally brightness of all pixels in the strip.

        If you don't supply a brightness value, the last value set for each pixel be kept.

        r: Amount of red: 0 to 255
        g: Amount of green: 0 to 255
        b: Amount of blue: 0 to 255
        brightness: Brightness: 0.0 to 1.0
        """

        for pixel in range(self.__striplength):
            self.pixel(pixel, r, g, b, brightness)

    # def set_sequence(self, sequence):
    #    """Set RGB values from a an FX sequence."""
    #    for index, rgb in sequence:
    #        self.set_pixel(index, *rgb)

    def clear(self):
        """Clear the pixel buffer."""
        for pixel in range(self.__striplength):
            self.__pixels[pixel][0:3] = [0, 0, 0]

    def atexit(self):
        """This will be called when the program exits"""
        if self.__clear_on_exit:
            self.clear()
            self.show()
            self.updatestatus = False

    def show(self):
        """Output to the strip."""

        for pixel in range(self.__strip.numPixels()):
            r, g, b, brightness = self.__pixels[pixel]
            self.__strip.setPixelColorRGB(pixel, r, g, b)

        self.__strip.show()
