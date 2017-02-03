# Make your room pretty with the flowing hue

import time

import math

from neopixel import *

# LED strip configuration:
LED_COUNT      = 60 * 4     # Number of LED pixels.
LED_PIN        = 18     # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Init light strip
    strip.begin()
    print ('Press Ctrl-C to quit.')
    while True:
        for progress in range(256):
            color = wheel(progress)
            for pixel in range(60 * 4):
                strip.setPixelColor(pixel, color)
            strip.show()
            time.sleep(30/1000.0)
