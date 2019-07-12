from rtlsdr import RtlSdr
from datetime import datetime
import asyncio
from matplotlib.mlab import psd
import threading
from multiprocessing import Process
import socket
import sys
import queue
import struct
import time

NFFT = 1024

# 4096 with 50% overlapping is good enough to get more than 1k samples per sec

fftResultQueue = queue.Queue() # FFT results
rawSampleQueue = queue.Queue() # raw samples


def signal_processing_run(rawSampleQueue):
    t1 = threading.currentThread() # signal on main thread exit to stop this thread
    timestamp1 = datetime.now()
    g_psd_scan = [0] * NFFT
    
    while getattr(t1, "do_run", True):

        timestamp2 = datetime.now()
        if (timestamp2 - timestamp1).total_seconds() > 1: 
            timestamp1 = datetime.now()
            print(g_psd_scan[0])
            g_psd_scan = [0] * NFFT

        if not rawSampleQueue.empty():
            #print ("rawSampleQueue size: " + str(rawSampleQueue.qsize()))
            p_samples = rawSampleQueue.get()
            psd_scan, f = psd(p_samples, NFFT=NFFT)
            for i in range(NFFT):
                if psd_scan[i] > g_psd_scan[i]:
                    g_psd_scan[i] = psd_scan[i] 
        time.sleep(0.01)
                
def clearQueue(q):
    while not q.empty():
        q.get()

async def get_samples(sdr, rawSampleQueue):
    counter = 0
    timestamp1 = datetime.now()
    # Get this many samples every time
    async for samples in sdr.stream():
        # keep queueing incomsing samples
        rawSampleQueue.put(samples)
        counter += 1
        timestamp2 = datetime.now()
        if (timestamp2 - timestamp1).total_seconds() > 1: 
            # To see if we missed any samples. Should be close to srate samples p/s
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'GETSAMPLES -', int((counter * 131072) / (timestamp2 - timestamp1).total_seconds()), 'samples p/s')
            counter = 0
            timestamp1 = datetime.now()
            
            


if __name__ == "__main__":
    try:
        ### setting up sdr streaming
        srate = 2400000 #sampling rate
        samplesperbit = 1000000 / 38400 / (1000000 / srate)
        sdr = RtlSdr()
        
        # Just like in URH
        sdr.freq_correction = 1
        sdr.sample_rate = srate
        sdr.center_freq = 61.000e6
        sdr.gain = 'auto'
        
        t1 = threading.Thread(target=signal_processing_run, args=(rawSampleQueue,))
        t1.start()
        
        
        # This is the main loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_samples(sdr, rawSampleQueue))

    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling tasks...")
        loop.stop()
        t1.do_run = False
        t1.join()
        
    
