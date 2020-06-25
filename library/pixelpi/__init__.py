__version__ = '0.0.2'

import RPi.GPIO as GPIO
import atexit
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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class PixelPi():
    def __init__(self, strip, stripsize, stripshape='straight', striptype='WS2812', brightness=1.0):
        """Initialise the LED Strip using the details given"""

        # Which strip connection is being used (1 to 4)
        if strip == 1:
            self.__controlpin = 10
            self.__channel = 0
            self.__onoffpin = 27
        elif strip == 2:
            self.__controlpin = 12
            self.__channel = 1
            self.__onoffpin = 4
        elif strip == 3:
            self.__controlpin = 21
            self.__channel = 0
            self.__onoffpin = 17
        elif strip == 4:
            self.__controlpin = 13
            self.__channel = 0
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

        if stripsize <= 0:
            raise ValueError("The strip length needs to be 1 or more.")
        self.__striplength = stripsize

        if brightness < 0 or brightness > 1.0:
            raise ValueError("The brightness must be between 0.0 and 1.0")
        self.__brightness = int(brightness * 255)

        self.__pixels = [[0, 0, 0, self.__brightness]] * self.__striplength

        self.__freq_hz = 800000
        self.__dma = 10
        self.__invert = False

        self.__strip = PixelStrip(self.__striplength, self.__controlpin, self.__freq_hz, self.__dma, self.__invert,
                                  self.__brightness, self.__channel, self.__striptype)
        self.__strip.begin()

        self.__clear_on_exit = True

        GPIO.setup(self.__onoffpin, GPIO.OUT)
        GPIO.output(self.__onoffpin, GPIO.LOW)
        self.__stripactive = True

        self.clear()

        atexit.register(self.atexit)

    def get_striplength(self):
        """Gets how many LEDs are in the strip"""
        return self.__striplength

    def get_striptype(self):
        """Gets the strip type"""
        return self.__striptype

    def get_stripnumber(self):
        """Gets which output the strip is attached to"""
        return self.__strip

    def get_pixel(self, pixel):
        """Gets the RGB and brightness value of a specific pixel."""
        if pixel > 0 and pixel < self.__striplength:
            r, g, b, brightness = self.__pixels[pixel]
        else:
            r, g, b, brightness = [0, 0, 0, 0]

        return r, g, b, brightness

    def get_stripupdatestatus(self):
        """Gets whether output is currently enabled for the strip"""
        return self.__stripactive

    def set_stripupdatestatus(self, status=True):
        """Sets whether the strip output is to be used

        status: On when True, Off when False
        """
        if status:
            GPIO.output(self.__onoffpin, GPIO.LOW)
            self.__stripactive = True
        else:
            GPIO.output(self.__onoffpin, GPIO.HIGH)
            self.__stripactive = False

    def set_clearonexit(self, status=True):
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

    def set_pixel(self, pixel, r, g, b, brightness=None):
        """Set the RGB value, and optionally brightness, of a single pixel.

        If you don't supply a brightness value, the last value will be kept.

        pixel: The pixel position in the strip
        r: Red: 0 to 255
        g: Green: 0 to 255
        b: Blue: 0 to 255
        brightness: Brightness: 0.0 to 1.0
        """
        if 0 <= pixel < self.__striplength:
            r, g, b = [int(c) & 0xff for c in (r, g, b)]

            if brightness is None:
                brightness = self.__pixels[pixel][3]

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
            self.set_pixel(pixel, r, g, b, brightness)

    def set_sequence(self, sequence):
        """Set RGB values from a an FX sequence."""
        for index, rgb in sequence:
            self.set_pixel(index, *rgb)

    def clear(self):
        """Clear the pixel buffer."""
        for pixel in range(self.__striplength):
            self.__pixels[pixel][0:3] = [0, 0, 0]

    def atexit(self):
        """This will be called when the program exits"""
        if self.__clear_on_exit:
            self.clear()
            self.show()
            self.set_stripupdatestatus(False)

    def show(self):
        """Output to the strip."""

        for pixel in range(self.__strip.numPixels()):
            r, g, b, brightness = self.__pixels[pixel]
            self.__strip.setPixelColorRGB(pixel, r, g, b)

        self.__strip.show()
