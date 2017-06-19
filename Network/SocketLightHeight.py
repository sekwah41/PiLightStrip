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

progress = 0



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

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


soc.connect((host, port))
while True:
    data = np.fromstring(soc.recv(1024 * 8),dtype=np.int16)
    #datasamp = np.fromstring(data,dtype=np.int16)
    if len(data):
        average = 0
        for i in range(0,len(data), datareduce):
            #print i
            if data[i] < 0:
                data[i] = -data[i]
            average = average + data[i]
        average = average / (len(data) / datareduce) * 2
        #print average
        levelcolor = dataToLight(average)
        #print levelcolor
        #progress = progress + 1
        increase = 20 * (levelcolor / float(LightInfo.LED_COUNT)) - 5
        if increase > 9:
            increase = increase - 9
            increase = increase / 2.0
            increase = increase + 9
        if increase > 14:
            increase = 14
        if increase > 0:
            progress = progress + increase

        color = wheel(int(progress % 256))

        #color = wheel(int (levelcolor / 240.0 * 255.0))
        for pixel in  range(levelcolor + 1, LightInfo.LED_COUNT):
            strip.setPixelColor(pixel,Color(0,0,0))
        for pixel in  range(levelcolor):
            strip.setPixelColor(pixel,color)
        strip.show()
soc.close()

#https://stackoverflow.com/questions/25505725/java-client-python-server-socket-programming