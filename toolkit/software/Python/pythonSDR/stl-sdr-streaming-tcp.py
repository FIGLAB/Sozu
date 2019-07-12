from rtlsdr import RtlSdr
from datetime import datetime
import asyncio
from matplotlib.mlab import psd
import threading
import socket
import sys
import queue
import json

NFFT = 64

ipAddress = 'localhost'
portNum = 8087

# 4096 with 50% overlapping is good enough to get more than 1k samples per sec

q2 = queue.Queue() # FFT results
q1 = queue.Queue() # raw samples

def server_run(sock, q2):
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        clearQueue(q2)
        print('connection from', client_address)
        print('queue cleared')
        
        while True:
            if not q2.empty():
                fftResults = q2.get()
                fftResults = fftResults.tolist()
                data = json.dumps(fftResults).encode()
                print(data)
                
                try:
                    connection.sendall(data)
                    
                except:
                    print('connection lost')
                    connection.close()
                    break
                
def clearQueue(q):
    while not q.empty():
        q.get()


async def get_samples(sdr, q1, q2):
    counter = 0
    timestamp1 = datetime.now()
    # Get this many samples every time
    async for samples in sdr.stream():
        q1.put(samples)
        counter += 1
        timestamp2 = datetime.now()
        if (timestamp2 - timestamp1).total_seconds() > 1:
            # To see if we missed any samples. Should be close to srate samples p/s
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'GETSAMPLES -', int((counter * 131072) / (timestamp2 - timestamp1).total_seconds()), 'samples p/s')
            counter = 0
            timestamp1 = datetime.now()

            psd_scan, f = psd(samples, NFFT=NFFT)
            q2.put(psd_scan)
            
            if q2.empty():
                print ("empty")
            else:
                print(q2.qsize())
                
            #print (psd_scan)
            

def main():

    ### setting up sdr streaming
    srate = 2400000 #sampling rate
    samplesperbit = 1000000 / 38400 / (1000000 / srate)
    sdr = RtlSdr()
    # Just like in URH
    sdr.freq_correction = 1
    sdr.sample_rate = srate
    sdr.center_freq = 100.000e6
    sdr.gain = 'auto'
    # Run check_samples in another thread to make sure we don't miss any samples
    
    ### setting up TCP server
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ipAddress, portNum)

    print('starting up on {} port {}'.format(*server_address))

    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)

    t1 = threading.Thread(target=server_run, args=(sock,q2))
    t1.start()

    # This is the main loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_samples(sdr, q1, q2))


if __name__ == "__main__":
    main()
