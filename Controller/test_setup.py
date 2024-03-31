from moku.instruments import MultiInstrument
from moku import Moku

# Replace MOKU_SERIAL with the serial number of your Moku:Go
#moku = Moku(ip="usb-c", serial='003975', force_connect=False, ignore_busy=False, persist_state=True, connect_timeout=1000, read_timeout=1000)


# Connect to your Moku by its ip address using Datalogger('192.168.###.###')
# or by its serial number using Datalogger(serial=123)
# i = Oscilloscope(serial='[fe80::7269:79ff:feb9:3e1e%19]')
# i = Oscilloscope('[fe80:0000:0000:0000:7269:79ff:feb9:3e1e%19]', force_connect=True)

m = MultiInstrument('[fe80:0000:0000:0000:7269:79ff:feb9:173a%20]', platform_id=2, force_connect=True)

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from simple_pid import PID