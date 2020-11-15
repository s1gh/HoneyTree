import time
from random import shuffle, sample
from rpi_ws281x import Color

def color_wipe_bottom_top(strip):
    for x in range(0, strip.numPixels()):
        strip.setPixelColor(x, Color(0,0,0))
        strip.show()

def color_wipe_top_bottom(strip):
    for x in range(0, strip.numPixels()):
        strip.setPixelColor(strip.numPixels() - x, Color(0,0,0))
        strip.show()

def color_wipe_rain(strip):
    available_pixels = sample([x for x in range(0, strip.numPixels())], strip.numPixels())

    for x in available_pixels:
        strip.setPixelColor(x, Color(0,0,0))
        strip.show()
    time.sleep(0.5)
