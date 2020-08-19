#!/bin/bash

if [ $(id -u) -ne 0 ]; then
  printf "Script must be run as root. Try 'sudo ./install.sh'\n"
  exit 1
fi

WORKING_DIR=$(pwd)

apt update
apt install -y python3-pip
apt install libatlas-base-dev python3-numpy libopenjp2-7 libopenjp2-7-dev libopenjp2-tools -y
pip3 install rpi.gpio rpi_ws281x gpiozero Pillow

cd $WORKING_DIR/library
sudo python3 setup.py install
cd $WORKING_DIR
