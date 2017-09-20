__author__ = 'sekwah'


import sys
import socket

import LightInfo
import numpy as np

from neopixel import *

if len(sys.argv) < 2:
    print("Select computer ip to connect to.\n\nUsage: %s IP ADDRESS" % sys.argv[0])
    sys.exit(-1)

print sys.argv[1]

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LightInfo.LED_COUNT, LightInfo.LED_PIN, LightInfo.LED_FREQ_HZ, LightInfo.LED_DMA, LightInfo.LED_INVERT, LightInfo.LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

datareduce = 5



soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = sys.argv[1] # Get local machine name
port = 6969                # Reserve a port for your service.

def dataToLight(average):
    value = int(average / 30000.0 * LightInfo.LED_COUNT * 2)
    if value < 0:
        return 0
    elif value > LightInfo.LED_COUNT - 1:
        return LightInfo.LED_COUNT - 1
    else:
        return value

soc.connect((host, port))

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LightInfo.LED_COUNT, LightInfo.LED_PIN, LightInfo.LED_FREQ_HZ, LightInfo.LED_DMA, LightInfo.LED_INVERT, LightInfo.LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

datareduce = 3

progress = 0

colormulti = 0

progtime = 0

def intense(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return 0
        elif pos < 170:
                pos -= 85
                return pos * 3
        else:
                pos -= 170
                return 255 - pos * 3

def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return Color(int(pos * 3 * (colormulti / 255.0)), int((255 - pos * 3) * (colormulti / 255.0)), 0)
        elif pos < 170:
                pos -= 85
                return Color(int((255 - pos * 3) * (colormulti / 255.0)), 0, int(pos * 3 * (colormulti / 255.0)))
        else:
                pos -= 170
                return Color(0, int(pos * 3 * (colormulti / 255.0)), int((255 - pos * 3) * (colormulti / 255.0)))

while True:
    #print data
    data = np.fromstring(soc.recv(1024 * 8), dtype=np.int16)
    if len(data):
        average = 0
        for i in range(0,len(data), datareduce):
            #print i
            if data[i] < 0:
                data[i] = -data[i]
            average = average + data[i]
        average = average / (len(data) / datareduce)
        #print average
        levelcolor = dataToLight(average)

        progtime = progtime + 1

        #print levelcolor
        #progress = progress + 1
        increase = 30 * (levelcolor / float(LightInfo.LED_COUNT)) - 9
        if increase > 0:
            progress = progress + increase

        #color = wheel(int (levelcolor / 240.0 * 255.0))
        for pixel in  range(LightInfo.LED_COUNT):
            colormulti = intense(int(progress + (pixel * 8.0)) % 256)
            if colormulti < 0:
                colormulti = 0
            color = wheel(int(progtime % 256))
            strip.setPixelColor(pixel,color)
        strip.show()

soc.close()
stream.close()

p.terminate()




