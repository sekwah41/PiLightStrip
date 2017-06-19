__author__ = 'sekwah'


import sys
import socket

import LightInfo
import numpy as np

from neopixel import *

soc = socket.socket()         # Create a socket object
host = "localhost" # Get local machine name
port = 6969                # Reserve a port for your service.

soc.connect((host, port))
while True:
    print len(soc.recv(1024 * 8))
soc.close()

#https://stackoverflow.com/questions/25505725/java-client-python-server-socket-programming