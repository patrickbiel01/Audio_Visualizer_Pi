# Audio Visualizer
An Audio Visualizer displayed using an LED Strip.

Demo:


## Hardware Requirements :
 * Raspberry Pi 4: [Link to buy](https://www.amazon.ca/gp/product/B084DQZP7P/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
 * WS2812b LED Programmable Strip: [Link to buy](https://www.amazon.ca/gp/product/B01CDTED80/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
 * Connector / Adapter : [Link to buy](https://www.amazon.ca/s?k=DC+adapter+cctv&linkCode=gs3&tag=787ca-20&ref=nb_sb_noss_2)
 * Diode with forward voltage drop = 0.7 Volt
 * 3 x 1 Male Connector Clips
 * 5 Volt, 2.5 Amp Power Supply 

## Hardware Setup
Since Pi GPIO Pins only output 3.5 V, we need to reduce the reference voltage in the strip or implement a level-shifter chip. In my project, I did soldered a 0.7 V Diode in series with the connector to the LED and Power Supply. When directed in the flow of the in order to make the reference voltage ~= 4.3 V. 


Here, is a good link to a [tutorial](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/) to setup the hardware configuration and initialize the developer tools in the Pi
![Hardware Setup Diagram](https://raw.githubusercontent.com/patrickbiel01/Audio_Visualizer_Pi/main/hardware_diagram.jpg)

## Installation
Dependencies:
* rpi_ws281x (LED Control)
* Librosa (Audio Analysis)
* Python 3.7.3 (Guaranteed, untested for other versions)
* Pip 21.1.1 (Guaranteed, untested for other versions)


```bash
# Install rpi_ws281x
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/python

# Setup a Virtual Environment
mkdir env
sudo -s
python3 -m venv env/
source env/bin/activate

# Install Librosa, Guide : [https://www.youtube.com/watch?v=ye96YO-lz_4]
sudo apt-get install llvm
LLVM_CONFIG=/usr/bin/llvm-config pip3 install llvmlite==0.32
pip3 install numpy==1.16.1 numba==0.49
pip3 install librosa

```

From here, move the audioVisualizer.py file to rpi_ws281x/python/examples

and the desired audio file to rpi_ws281x/python

## Run
```bash
# Go to proper directory
cd rpi_ws281x/python
# Enter Root Mode
sudo -s
# Activate Virtual Environment
source env/bin/activate
# Run script
python examples/audioVisualizer.py
```

## Issues
If you have any bugs or feature requests, please submit an [issue](https://github.com/patrickbiel01/Audio_Visualizer_Pi/issues).

## Contribution
If you wish to contribute, fork my project and create a [pull request](https://github.com/patrickbiel01/Audio_Visualizer_Pi/pulls)

## License
**Audio_Visualizer_Pi** is released under the MIT LICENSE. See [LICENSE](https://github.com/patrickbiel01/Audio_Visualizer_Pi/blob/main/LICENSE) for details
