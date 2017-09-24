# Make your room pretty with the flowing hue

import time

import LightInfo

from neopixel import *


def wheel(pos):
    if pos < 85:
        return Color(int(pos * 3), int(255 - pos * 3), 0)
    elif pos < 170:
        pos -= 85
        return Color(int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return Color(0, int(pos * 3), int(255 - pos * 3))

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LightInfo.LED_COUNT, LightInfo.LED_PIN, LightInfo.LED_FREQ_HZ, LightInfo.LED_DMA, LightInfo.LED_INVERT, LightInfo.LED_BRIGHTNESS)
    # Init light strip
    strip.begin()
    print ('Press Ctrl-C to quit.')
    while True:
        for progress in range(256):
            for pixel in range(LightInfo.LED_COUNT):
                strip.setPixelColor(pixel, wheel(progress + (pixel * 0.4)))
            strip.show()
            time.sleep(30/1000.0)
