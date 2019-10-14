# Sozu Toolkit

This is a quick start quide for Sozu toolkit.

## What are included in the toolkit
*  A Sozu tag powered by a small [solar panel](https://www.digikey.com/product-detail/en/panasonic-bsg/AM-8801CAR/869-1016-ND/2165201)
*  One alligator clip
*  [RTL-SDR + antenna](https://www.amazon.com/dp/B011HVUEME/ref=cm_sw_em_r_mt_dp_U_lSCGCbVDHKKQQ)

## Usage

### Step 1: Connect the SDR with antenna (two long ones), and connect it to the laptop:

<img src="./images/assembleantenna.gif" alt="" width="499"/>

### Step 2: Install software

Sozu receiver is based on SDR. In this tutorial, we will use RTL-SDR. The easiest way to get data out of RTL-SDR is to use [pystlsdr](https://nocarryr.github.io/pyrtlsdr/) -- A Python wrapper for librtlsdr (a driver for Realtek RTL2832U based SDR’s). Python3 is required (3.7.4 was tested).

Steps to below to install librtlsdr and run Sozu demo code:

1. Install pyrtlsdr via [pip](https://pip.pypa.io/en/stable/):  

```bash
pip install pyrtlsdr
```

2. Install librtlsdr via [brew](https://brew.sh):  

```bash
brew install librtlsdr
```

2. Download and install Processing from [https://processing.org](https://processing.org)


3. Download Project Sozu source code from the [Github Page](https://github.com/FIGLAB/Sozu) or

```bash
git clone git@github.com:FIGLAB/Sozu.git
```

4. Now plug in the SDR with the antenna connected (through USB) and get the RF signal from your environment by running the python code (./software/Python/demo_waterfall.py):

```bash
python demo_waterfall.py
```
<img src="./images/waterfall.gif" alt="" width="499"/>

If you can see the above output on your python window, you are ready to receive RF signals from Sozu tags!

### Step 3: Deploy Sozu tag in the environment
1. Deploy harvesters in the environment (if you are looking for examples, we have a [webpage](https://FIGLAB.com/) which shows how we harvest energy from a wide range of objects)

2. Make sure harvester provides higher than 1.5 Volts from the activity that you are interested in sensing using the multimeter.

3. Connect the energy harvester to the Sozu tag.

### Step 4: Get the Sozu signal in Processing

1. Run the Python server code(./software/Python/demo_waterfall_server.py):

<img src="./images/pythonserver.gif" alt="" width="499"/>

2. Tune the center frequency of your SDR around the Sozu tag frequency (labeled on the back of the tag), until you see its signal on the waterfall chart:

<img src="./images/search.gif" alt="" width="499"/>

3. Run the Processing client code. Now you should see Sozu tag's signal shown in the Processing app:

<img src="./images/processing.gif" alt="" width="499"/>

After you can see the signal in the processing app, you are ready to make applications!


## Debug Sozu

### Gqrx
[Gqrx](http://gqrx.dk) is a useful software to interface SDRs with a nice UI, which you can use and tune many parameters (e.g., sampling rate, center frequency, averaging etc.) for debug.

<img src="./images/gqrx.png" alt="" width="499"/>

### Known issues
#### OSError: Error code -3 when opening SDR (device index = 0)
Solution: Unplug the SDR from the USB, and plug it back in.

#### AttributeError: dlsym(RTLD_DEFAULT, rtlsdr_get_device_count): symbol not found
Solution: Try brew install librtlsdr again.
