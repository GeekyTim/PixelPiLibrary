import time
from subprocess import check_call

from gpiozero import Button


class PixelPiButton:
    """
    A class to handle the button on the PixelPi board for the Raspberry Pi.

    If no parameters are supplied, the Raspberry Pi will be rebooted after the button has been held for 0.5 seconds, or
    will be shut down if the button is held for 2 seconds or all.

    Alternatively, a local Class can be created with two methods to handle a short and a long press. Create an instance
    of the class and supply the class, method names and press-times to this class. For example::

        class MyButtons:
        def __init__(self, strips=None):
            self.__strips = strips

        def clear(self):
            try:
                if self.__strips is not None:
                    for strip in self.__strips:
                        strip.clearLEDs()
                        strip.showLEDs()
            except:
                raise AttributeError('The strip list contained an error.')

        def whitelights(self):
            try:
                if self.__strips is not None:
                    for strip in self.__strips:
                        strip.setLEDs(rgb=(255, 255, 255))
                        strip.showLEDs()
            except:
                raise AttributeError('The strip list contained an error.')

    Create an instance of the MyButtons class::

        mybuttons = MyButtons([strip1, strip2, strip3, strip4])

    Then create an instance of the PixelPiButton class, passing in the local class and methods::

        button = PixelPiButton(callingclass=mybuttons, shortpresstime=0.5, shortpress="clear", longpresstime=1.0,
        longpress="whitelights")

    When the button is held for shortpresstime, the 'clear' method will be executed, unless it is held for
    longpresstime after which 'whitelights' will be called.

    :type callingclass: object
    :param callingclass: The 'local' class.

    :type shortpresstime: float
    :param shortpresstime: The short press time.

    :type shortpress: str
    :param shortpress: The method in class ``callingclass`` that is called after the button has been pressed for
        shortpresstime seconds.

    :type longpresstime: float
    :param longpresstime: The long press time.

    :type longpress: str
    :param longpress: The method in class ``callingclass`` that is called after the button has been pressed for
        longpresstime seconds.
    """

    def __init__(self, callingclass=None, shortpresstime=0.5, shortpress=None, longpresstime=2.0, longpress=None):
        self.__buttonpin = 26

        if shortpresstime >= longpresstime:
            raise ValueError('The short press time must be longer than the long press time.')
        elif shortpresstime <= 0 or longpresstime <= 0:
            raise ValueError('The short and long press times must more than 0.0 seconds.')

        self.__shortpresstime = shortpresstime
        self.__longpresstime = longpresstime
        self.__thebutton = Button(self.__buttonpin)

        try:
            if shortpress is None:
                self.__shortpress = getattr(self, "__reboot")
            else:
                self.__shortpress = getattr(callingclass, shortpress)

            if longpress is None:
                self.__longpress = getattr(self, "__shutdown")
            else:
                self.__longpress = getattr(callingclass, longpress)
        except:
            raise AttributeError('PixelPiButton: There is a problem with the class methods. '
                                 'Check that the callingclass and methods are correct.')

        self.__thebutton.when_pressed = self.__pushbutton

    @staticmethod
    def __shutdown():
        check_call(['sudo', 'poweroff'])

    @staticmethod
    def __reboot():
        check_call(['sudo', 'reboot'])

    def __pushbutton(self):
        start_time = time.time()
        now_time = time.time()

        while self.__thebutton.is_active:
            now_time = time.time()

        diff = now_time - start_time

        if diff >= 2.0:
            self.__longpress()
        elif diff >= 0.5:
            self.__shortpress()
