#!/bin/bash
sudo apt update -y && sudo apt upgrade -y
sudo apt install python3-pip -y
sudo apt-get install pigpio python-pigpio python3-pigpio -y
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo "dtoverlay=i2c-gpio,bus=5,i2c_gpio_sda=10,i2c_gpio_scl=11" >> /boot/config.txt


