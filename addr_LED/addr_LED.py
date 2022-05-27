# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


class NeoPixel:
    def __init__(self):
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        self.pixel_pin = board.D18

        # The number of NeoPixels
        self.num_pixels = 2

        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.ORDER = neopixel.RGB

        self.brightness = 0.5
        
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=False, pixel_order=self.ORDER
        )


    def statusLED_front(self, colors): # note that colors is a 1x3 RGB list
        self.pixels[0] = colors
        
    def statusLED_back(self, colors):
        self.pixels[1] = colors

    def statusLED_both(self, colors):
        self.pixels.fill(colors)

    def statusLED_show(self):
        self.pixels.show()


if __name__ == "__main__":
    addrLED = NeoPixel()

    addrLED.statusLED_front([255,255,255])
    addrLED.statusLED_back([255,0,0])
    addrLED.statusLED_show()

    time.sleep(2)

    addrLED.statusLED_both([0,0,0])
    addrLED.statusLED_show()
