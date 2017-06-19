import time

__author__ = 'sekwah'

import pyaudio
import socket
from socket import error as socket_error

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()

outData = ""

def callback(in_data, frame_count, time_info, status):
    global datasamp
    global outData
    outData = in_data
    return (in_data, pyaudio.paContinue)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

frames = []

looping = True

#network stuff
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.43.110"  # Get local machine name
port = 6969  # Reserve a port for your service.
soc.bind((host, port))  # Bind to the port
soc.listen(5)  # Now wait for client connection.
print "Waiting for connection"
while True:
   c, addr = soc.accept()     # Establish connection with client.
   print 'Got connection from', addr
   #c.send('Thank you for connecting')
   looping = True
   while looping:
       # print outData
       try:
           #print len(outData)
           c.send(outData)
       except socket_error as serr:
           print serr.errno
           c.close()
           looping = False
       time.sleep(30.0 / 1000)


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()