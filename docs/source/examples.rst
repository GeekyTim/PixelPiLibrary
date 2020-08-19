============
Example Code
============
Example code has been supplied to illustrate the methods available.

.. Note::
  Remember to change the Strip definition to suit the LEDs connected. Each of the four terminals may use a
  different LED type and shape.

Run the code using::

 sudo python3 example.py

Rainbow
-------

Displays a moving rainbow on your LEDs.

.. literalinclude:: ../../examples/rainbow.py
   :language: python

Shifting LEDs
-------------
The LED colours can be shifted by a number of LEDs and direction:

Shifting LED Strings
^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: ../../examples/string_shift.py
   :language: python

Shifting LED Matrices
^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: ../../examples/matrix_shift.py
   :language: python

Mirroring in an Axis
--------------------
Mirroring LED Strings
^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: ../../examples/string_mirror.py
   :language: python

Mirroring LED Matrices
^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: ../../examples/matrix_mirror.py
   :language: python

Displaying an Image
-------------------
Displaying Images of LED Matrices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. literalinclude:: ../../examples/matrix_image.py
   :language: python

.. :Note::
  The image must be formatted in RGB format.  See
        `Pillow image file formats <https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html>`_
  You may manipulate the

:Note: You can of course display an image on an LED string by supplying a 1 by x image.
