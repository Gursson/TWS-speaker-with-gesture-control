#!/usr/bin/python3

import argparse
import signal
import sys
import time
import logging
from rpi_rf import RFDevice

import gpiozero
import RPi.GPIO as GPIO

#SETUP GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=13,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))
sleepit = 2
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if ( abs(rfdevice.rx_pulselength -250) < 10 ):
            if (abs(rfdevice.rx_code - 12345678) < 100):
                logging.info(str(rfdevice.rx_code) +
                             " [pulselength " + str(rfdevice.rx_pulselength) +
                             ", protocol " + str(rfdevice.rx_proto) + "]")
                print(f"~~~~~~> Volume Down")
                GPIO.output(16, False)
                time.sleep(0.15)
                GPIO.output(16, True)
                time.sleep(0.15)
                GPIO.output(16, False)
                
                time.sleep(sleepit)
            if (abs(rfdevice.rx_code -  23456789) < 100):
                logging.info(str(rfdevice.rx_code) +
                             " [pulselength " + str(rfdevice.rx_pulselength) +
                             ", protocol " + str(rfdevice.rx_proto) + "]")
                print("~~~~~~> Previous song" )
                GPIO.output(16, False)
                time.sleep(0.1)
                GPIO.output(16, True)
                time.sleep(2.2)
                GPIO.output(16, False)
                time.sleep(0.1)
                
            if (abs(rfdevice.rx_code - 34567890) < 100):
                logging.info(str(rfdevice.rx_code) +
                             " [pulselength " + str(rfdevice.rx_pulselength) +
                             ", protocol " + str(rfdevice.rx_proto) + "]")
                print("~~~~~~> Pause/Play")
                GPIO.output(16, False)
                time.sleep(0.1)
                GPIO.output(16, True)
                time.sleep(0.1)
                GPIO.output(16, False)
                time.sleep(0.1)
                GPIO.output(16, True)
                time.sleep(0.1)
                GPIO.output(16, False)
                                
        else:
            #print(f"Bläh: {rfdevice.rx_pulselength}")
            pass
            
    time.sleep(0.01)

rfdevice.cleanup()
