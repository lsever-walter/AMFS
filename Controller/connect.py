from moku.instruments import Oscilloscope
from moku import Moku

# Replace MOKU_SERIAL with the serial number of your Moku:Go
#moku = Moku(ip="usb-c", serial='003975', force_connect=False, ignore_busy=False, persist_state=True, connect_timeout=1000, read_timeout=1000)


# Connect to your Moku by its ip address using Datalogger('192.168.###.###')
# or by its serial number using Datalogger(serial=123)
# i = Oscilloscope(serial='[fe80::7269:79ff:feb9:3e1e%19]')
i = Oscilloscope('[fe80:0000:0000:0000:7269:79ff:feb9:3e1e%19]', force_connect=True)

