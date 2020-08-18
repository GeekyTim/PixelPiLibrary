================================
Using the PixelPi Python Library
================================
The PixelPi Library is intended to be used with the PixelPi PCB from Hut 8 Designs.

If you have not already installed the library, see :ref:`Installing the Python Library`

Creating a Strip Object
-----------------------

.. autoclass:: pixelpi.Strip
   :members: getLength, getWidth, getHeight, getStripType, getStripNumber, getUpdateStatus, getStripPattern

Setting LED Colours
-------------------
.. automethod:: pixelpi.Strip.showStrip

.. automethod:: pixelpi.Strip.setLED

.. automethod:: pixelpi.Strip.clearStrip

.. automethod:: pixelpi.Strip.setBrightness

.. automethod:: pixelpi.Strip.setUpdateStatus

.. automethod:: pixelpi.Strip.getLED

.. automethod:: pixelpi.Strip.setImage

.. automethod:: pixelpi.Strip.setStripPattern

.. automethod:: pixelpi.Strip.rotateStrip

.. automethod:: pixelpi.Strip.reflectStrip

