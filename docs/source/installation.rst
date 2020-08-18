=============================
Installing the Python Library
=============================
This PixelPi Library is a fork of the Pimoroni (http://pimoroni.com) Plasma code (https://github.com/pimoroni/plasma),
massively simplified and extensively modified to be used with the PixelPi Raspberry Pi 'small' HAT from Hut 8 Designs.

:Note: The library has been designed to only work with Python 3.

Before installing the library, you need to prepare you Raspberry Pi OS. These instructions assume you are starting with
the latest version of the Raspberry Pi OS Lite.

It is always good to start from an updated OS, so log in and run the following commands::

  sudo apt update && sudo apt upgrade

config.txt
==========
The PixelPi board needs some of the Raspberry Pi interfaces turned on, and one turned off. The Raspberry Pi audio
and the PWM channels used by the PixelPi cannot be used at the same time, so if you are using strip outputs 2 and 4
you need to disable audio on the Pi. Do the following to ensure the audio is completely turned off by editing the boot
config file with::

 sudo nano /boot/config.txt

The uncomment this lines, and add the second::

 hdmi_force_hotplug=1
 hdmi_force_edid_audio=1

Ensure the following line is commented by placing a # at the start::

 #dtparam=audio=on

Uncomment or add the following to in the optional hardware interfaces::

 dtparam=spi=on

Disable Sound in the Kernel
===========================

You will also need to edit the kernel module blacklist::

 sudo nano /etc/modprobe.d/snd-blacklist.conf

Add the following line::

 blacklist snd_bcm2835

Using strip4
============

Strip 4 uses SPI. You should increase the buffer size to handle most eventuallities of LED strip length. Edit the
boot commandline file::

 sudo nano /boot/cmdline.txt

Add the following to the end of the only line to increase the SPI buffer size:

 spidev.bufsiz=32768

Reboot
======
You need to reboot your Raspberry Pi for the above changes to take effect::

 sudo reboot

Installing the PixelPi Library
==============================
The PixelPi library is available on GitHub. to retrieve it you need to install git::

 sudo apt install git -y

The library can be downloaded then installed (with all prerequisites) with the following commands::

 cd ~
 git clone http://github.com/geekytim/PixelPiLibrary
 cd ~/PixelPiLibrary
 sudo bash install.sh



