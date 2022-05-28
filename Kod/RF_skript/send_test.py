#!/usr/bin/env python3

import logging
import time

from rpi_rf import RFDevice

rfdevice = RFDevice(4)
rfdevice.enable_tx()

code = 1
code2 = 55
logging.info(
            " [protocol: " + str(1) +
             ", pulselength: " + str(350) +
             ", length: " + str(None) +
            ", repeat: " + str(10) + "]")


	
rfdevice.tx_code(code)
print("Sending", code)
time.sleep(2)
rfdevice.tx_code(code2)
print("Sending", code2)
#rfdevice.tx_code(3) #skickar i slutet för att inte spammas med skick.
	
	
	
	

rfdevice.cleanup()
