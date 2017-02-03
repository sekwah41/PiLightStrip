# PiLightStrip
Lightshows for the AdaFruit light strip

Download the https://github.com/jgarff/rpi_ws281x as it is a needed library

One major issue with this setup is the lights use the audio pins to run, so you should buy a usb audio driver to run this.

Will probably make a music/dj system to work with mobile over a web server at some point reusing this code

To run the programs, just alter the file in each folder called LightInfo to be what your system has

Shopping list if u wanna build something like this

Adafruit NeoPixel Digital RGB LED Strip
e.g. https://www.adafruit.com/products/1461
Can be any length, just has to be neopixels as its using a library to run neopixels
Depending on the power you may need extra power packs, just make sure they are 5V and whatever amps you need, if you connect them in parallel remember they add the amps together :)

Any usb Audio jack (may work if your hdmi tv has audio, ive not tested hdmi audio cauz the jack on my tv is glitched, also normal audio jack is broken while using this)

Speakers (Generally computer speakers come with a male to male, just make sure you have a way of plugging in the audio :) )

Raspberry Pi V3 (prefferably, should work on any with the 40 pin connector or any type of GPIO pins that accept PWM0)



Note:

Personally I ssh into my Pi. If you have firewall issues such as on a uni network or don't want to port forward then you can just route it through some sort of other accessible server you own.
(I'll document how to set that up if enough people want to know about it)


