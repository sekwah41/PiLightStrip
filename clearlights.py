# Designed to reset all the lights.
import time

import LightInfo

from neopixel import *

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LightInfo.LED_COUNT, LightInfo.LED_PIN, LightInfo.LED_FREQ_HZ, LightInfo.LED_DMA, LightInfo.LED_INVERT, LightInfo.LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

strip.show()

