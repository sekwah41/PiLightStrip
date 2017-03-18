import pyaudio
import numpy as np
import decoder
#import pylab
import time

from neopixel import *


# LED strip configuration:
LED_COUNT      = 60 * 4     # Number of LED pixels.
LED_PIN        = 18     # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)



RATE = 44100
CHUNK = int(RATE/60) # RATE / number of updates per second

def dataToLight(average):
    value = int(average / 6000.0 * 255)
    if value < 0:
        return 0
    elif value > 255:
        return 255
    else:
        return value

def soundplot(strip, stream):
    t1=time.time()
    data = np.fromstring(stream.read(CHUNK,exception_on_overflow = False),dtype=np.int16)
    #print len(data)
    average = 0
    for i in data:
        #print i
        if i < 0:
            i = -i
        average = average + i
    average = average / len(data)
    #print average
    for pixel in  range(60 * 4):
        strip.setPixelColor(pixel,Color(0,dataToLight(average),0))
    strip.show()

    #string = ""
    #for i in range(int(average / 3000.0 * 20.0)):
    #string = string + "="
    #print string
    #print("took %.02f ms"%((time.time()-t1)*1000))

datasamp = []

datareduce = 3

progress = 0

dc = decoder.open(sys.argv[1])

def callback(in_data, frame_count, time_info, status):
    global datasamp
    data = dc.readframes(frame_count)
    datasamp = np.fromstring(data,dtype=np.int16)
    return (data, pyaudio.paContinue)

if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1, input_device_index=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK, stream_callback=callback)
    #for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
    #print datasamp

    while stream.is_active():
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
            #print levelcolor
            #progress = progress + 1
            increase = 20 * (levelcolor / float(LightInfo.LED_COUNT)) - 5
            if increase > 0:
                progress = progress + increase

            color = wheel(int(progress % 256))

            #color = wheel(int (levelcolor / 240.0 * 255.0))
            for pixel in  range(levelcolor + 1, LightInfo.LED_COUNT):
                strip.setPixelColor(pixel,Color(0,0,0))
            for pixel in  range(levelcolor):
                strip.setPixelColor(pixel,color)
            strip.show()
        time.sleep(30.0/1000)

    stream.stop_stream()
    stream.close()
    p.terminate()


