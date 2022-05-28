#!/usr/bin/env python3

import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)
def Volume_down():
    print("inside Volume_down")
    
    
def Prev_song():
    print("inside Prev_song")
def PP():
    print("inside PP")    
    

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')

args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(4)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(4))
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
    time.sleep(0.5)
    if rfdevice.rx_code == 55 and rfdevice.rx_code_timestamp != timestamp:
        Volume_down()
        
        
        
        
rfdevice.cleanup()
