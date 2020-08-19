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
.. automethod:: pixelpi.Strip.setLED

.. automethod:: pixelpi.Strip.getLED

.. automethod:: pixelpi.Strip.setBrightness

.. automethod:: pixelpi.Strip.setImage

.. automethod:: pixelpi.Strip.setPattern

.. automethod:: pixelpi.Strip.clearStrip


Manipulating LED Colours
------------------------
.. automethod:: pixelpi.Strip.rotateStrip

.. automethod:: pixelpi.Strip.reflectStrip

Controlling Strip Updates
-------------------------
.. automethod:: pixelpi.Strip.showStrip

