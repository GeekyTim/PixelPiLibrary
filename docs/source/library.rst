================================
Using the PixelPi Python Library
================================
The PixelPi Library is intended to be used with the PixelPi PCB from Hut 8 Designs.

If you have not already installed the library, see :ref:`Installing the Python Library`

Creating a Strip Object
-----------------------
.. module:: pixelpi

.. autoclass:: pixelpi.Strip
   :members: getLength, getWidth, getHeight, getStripType, getStripNumber, updateStatus

Setting LED Colours and Brightness
----------------------------------
.. automethod:: pixelpi.Strip.setLEDs

.. automethod:: pixelpi.Strip.getLEDs

.. automethod:: pixelpi.Strip.clearLEDs

Manipulating LED Colours
------------------------
.. automethod:: pixelpi.Strip.shift

.. automethod:: pixelpi.Strip.mirror

Updating LEDs
-------------
.. automethod:: pixelpi.Strip.showLEDs

