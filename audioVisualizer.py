import math

import librosa
import numpy as np
import time
from rpi_ws281x import *



filename = "Swif7-Don'tWannaSleep.mp3"
NUM_LEDS = 60
window_size = 2048
hop_length = 64



# Setup:
    # sudo -s
    # Setup virtual environemt
    # source env/bin/activate
    # Install librosa using guide : https://www.youtube.com/watch?v=ye96YO-lz_4
    # Make sure to use latest version of numpy and move script to examples directory
    # Run script: python examples/audioVisualizer.py




# Helper Functions & Stuff
def getFreqBins(spec, freqs) :
        freqBins = []
        size = len(freqs)
        increment = size / NUM_LEDS
        for i in range(NUM_LEDS):
            freqBins.append(i*increment)

        return freqBins


def amplitudeToColour(amplitude, freq) :
        r = 0
        g = 0
        b = 0

        # Bass - Blue
        #if freq >= 20 and freq < 250 :
        b = int( 255 * amplitude )
        # Midrange - Green
        #if freq >= 250 and freq < 4000 :
        #g = int( 255 * amplitude )
        # Presence / Brilliance - Red
        #if freq >= 250 and freq < 4000 :
        #r = int( 255 * amplitude )


        col = Color(r, g, b)
        return col


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)




# Setting up led
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # TODO: Check this, GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()



# Load audio
time_series, sample_rate = librosa.load(filename)
LEN_SONG = librosa.get_duration(y=time_series, sr=sample_rate)

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs( librosa.stft(time_series, hop_length=hop_length, n_fft=window_size) )

# converting the matrix to map linearly to human perception
spectrogram = librosa.amplitude_to_db(stft, ref=np.max) # 0db max, more -db val => closer to 0
spectrogram = np.reciprocal( np.abs( np.subtract(spectrogram, 1) ) ) # 1 / |x-1|, this maps the amplitudes from 0-1 with 1 being most intense



# Get axis values
freqs = librosa.core.fft_frequencies(n_fft=window_size)
times = librosa.core.frames_to_time(spectrogram[0], sr=sample_rate, n_fft=window_size, hop_length=hop_length)


# Get freqs to map to 60 leds
freqBins = getFreqBins(spectrogram, freqs)


# Get the max value for each freq during the song
max_amps = []
for i in range(len(freqs)) :
        freqTime = spectrogram[i, :]
        max_amps.append( np.max(freqTime) )


# Show start prompt
print("Staring Visualization of ", filename, " for ", LEN_SONG, " seconds")



# Start timer
timeStart = time.time()
currTime = time.time() - timeStart
firstTime = True


while currTime < LEN_SONG :

        time_idx = int(currTime * sample_rate / hop_length)

        led = 0
        for fft_bin in range(len(freqBins)) :
                amplitude = spectrogram[fft_bin, time_idx]
                # Convert to rgb value
                col = amplitudeToColour( amplitude, freqs[fft_bin] );

                #if fft_bin == 15 :
                        #print("Amplitude = ", amplitude, " and intensity = ", int( 255 * amplitude ), " and sample_rate = ", sample_rate, " @ timestep = ", time_idx)
                        #print("\n\n")

                # Write rgb value to led
                strip.setPixelColor(led, col)

                led += 1

        strip.show()
        firstTime = False

        currTime = time.time() - timeStart





#clear leds
colorWipe(strip, Color(0,0,0), 10)




iprint("This is the end")
