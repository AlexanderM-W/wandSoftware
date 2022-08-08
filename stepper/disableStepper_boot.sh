#!/bin/bash

#   Exports pin to userspace
echo "14" > /sys/class/gpio/export  

# Sets pin 18 as an output
echo "out" > /sys/class/gpio/gpio14/direction

# Sets pin 18 to high
echo "1" > /sys/class/gpio/gpio14/value

# Sets pin 18 to low
#echo "0" > /sys/class/gpio/gpio14/value 