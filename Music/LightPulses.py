"""PyAudio Example: Play a WAVE file."""

import pyaudio
import decoder
import sys
import time
import numpy as np

import LightInfo

from neopixel import *

CHUNK = 1024



if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

print sys.argv[1]

dc = decoder.open(sys.argv[1])

p = pyaudio.PyAudio()

datasamp = []

def callback(in_data, frame_count, time_info, status):
    global datasamp
    data = dc.readframes(frame_count)
    datasamp = np.fromstring(data,dtype=np.int16)
    return (data, pyaudio.paContinue)

def dataToLight(average):
    value = int(average / 30000.0 * LightInfo.LED_COUNT * 2)
    if value < 0:
        return 0
    elif value > LightInfo.LED_COUNT - 1:
        return LightInfo.LED_COUNT - 1
    else:
        return value

stream = p.open(format=p.get_format_from_width(dc.getsampwidth()),
                channels=dc.getnchannels(),
                rate=dc.getframerate(),
                output_device_index=2,
                frames_per_buffer=CHUNK,
                output=True,
                input=False,
                stream_callback=callback)

stream.start_stream()

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

while stream.is_active():
    #print datasamp
    if len(datasamp):
        average = 0
        for i in range(0,len(datasamp), datareduce):
            #print i
            if datasamp[i] < 0:
                datasamp[i] = -datasamp[i]
            average = average + datasamp[i]
        average = average / (len(datasamp) / datareduce)
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
    time.sleep(30.0/1000)

stream.stop_stream()
stream.close()

p.terminate()




