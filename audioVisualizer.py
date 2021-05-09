import math

import librosa
import numpy as np
import time
from sys import stdout
from rpi_ws281x import *



# Useful information
filename = "Swif7-Don'tWannaSleep.mp3"
NUM_LEDS = 60
window_size = 2048
hop_length = 64



# Script Setup:
    # sudo -s
    # Setup virtual environemt
    # source env/bin/activate
    # Install librosa using guide : https://www.youtube.com/watch?v=ye96YO-lz_4
    # Make sure to use latest version of numpy and move script to examples directory
    # Run script: python examples/audioVisualizer.py




# Divide up the STFT frequency indexes and map them to the LEDs
def getFreqBins(spec, freqs) :
	freqBins = []
	size = len(freqs)
	increment = size / NUM_LEDS
	for i in range(NUM_LEDS):
		freqBins.append(i*increment)

	return freqBins


# Scales down an value by a factor if it's less than a threshold
def lowAmplitudeAttenuation(amplitude, threshold, shrink_factor) :
	# 0 < amplitude, threshold, shrink_factor < 1
	if amplitude <= threshold :
		amplitude = shrink_factor * amplitude

	return amplitude


# Maps the amplitude to a corresponding rgb value
	# Try and scale down smaller values so the peaks are more apparent
	# Uses a bell-curve like function to make a continous spectrum on the leds where:
		# Bass = Blue, Mid = Green, High = Red
def amplitudeToColour(amplitude, freq) :
	r = 0
	g = 0
	b = 0

	# Scale amplitudes below 0.5 by 0.5
	tHold = 0.5
	scale_factor = 0.5
	amplitude = lowAmplitudeAttenuation(amplitude, tHold, scale_factor)

	# Scale amplitudes below 0.3 by 0.3
	tHold = 0.3
	scale_factor = 0.3
	amplitude = lowAmplitudeAttenuation(amplitude, tHold, scale_factor)

	# Bass - Blue
	bassFactor = np.exp( -1 * np.power( freq/300 , 4) ) # e^(-(x/300)^4)
	b = int( 255 * amplitude * bassFactor )
        
	# Midrange - Green
	midFactor = np.exp( -1 * np.power( (freq-2500)/2250 , 12) ) #  e^(-( (x-2500)/2250 )^12 )
	g = int( 255 * amplitude * midFactor )
	
	# Presence / Brilliance - Red
	if freq >= 4000 :
		r = int( 255 * amplitude )
	

	return Color(r, g, b)




# Writes a colour value to all leds
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)




# Setting up leds
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
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
print("Staring Visualization of ", filename, "in: ")
for i in range(3,0,-1):
    stdout.write("\r%d" % i)
    stdout.flush()
    time.sleep(1)
print("\nGo!\n")


# Start timer
timeStart = time.time()
currTime = time.time() - timeStart


# Writing the STFT ampiltudes to leds until song is done
while currTime < LEN_SONG :

	# Get the proper STFT time index from our current time
	time_idx = int(currTime * sample_rate / hop_length)

	# Display Current Song Progress
	stdout.write("\rCurrent Progress: %lf seconds" % currTime)
	stdout.flush()

	# Writing Colour-Mapped Amplitude to all LEDs
	led = 0
	for fft_bin in range(len(freqBins)) :
                # Retrieve amp from STFT
		amplitude = spectrogram[fft_bin, time_idx]

		# Convert to rgb value
		col = amplitudeToColour( amplitude, freqs[fft_bin] );

		# Write rgb value to led
		strip.setPixelColor(led, col)

		led += 1

	# Display written values
	strip.show()

	# Update progress
	currTime = time.time() - timeStart



# Clear LEDs
colorWipe(strip, Color(0,0,0), 10)



print("\n")
print("Done!")

