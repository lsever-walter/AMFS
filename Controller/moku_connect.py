from simple_pid.pid import *


from moku.instruments import MultiInstrument
from moku.instruments import Oscilloscope, Datalogger


import os
import time


import matplotlib as plt
from jax_adjacent.base.applets.real_time_plot_applet import *



m = MultiInstrument('192.168.###.###', platform_id=2)
try:
    dl = m.set_instrument(1, Datalogger)
    osc = m.set_instrument(2, Oscilloscope)

    connections = [dict(source="Input1", destination="Slot1InA"),
               dict(source="Slot2OutA", destination="Output1")]
    
    
    m.set_connections(connections=connections)

    print(m.set_connections(connections=connections))
except Exception as e:
    raise e

dl = m.set_instrument(1, Datalogger)
osc = m.set_instrument(2, Oscilloscope)


'''Take Data and Generate PID signal'''

PID_Generator = PID()
try:

    #only want stream from channel 1

    dl.disable_channel(2)

    # set the sample rate to 100KSa/s
    dl.set_samplerate(10e5)

    # stream the data for 10 seconds.. 
    #should replace this with a loop
    dl.start_streaming(10)

    # Set up the plotting parameters
    plt.ion()
    plt.show()
    plt.grid(b=True)
    plt.ylim([-1, 1])

    line1, = plt.plot([])

    # Configure labels for axes
    ax = plt.gca()

    # This loops continuously updates the plot with new data
    while True:
        # get the chunk of streamed data
        data = dl.get_stream_data()
        signal = PID_Generator.__call__(data['time'][-1])
        osc.set_power_supply(1,enable=True,voltage=2, current=0.1)
        if data:
            plt.xlim([data['time'][0], data['time'][-1]])
            # Update the plot
            line1.set_ydata(data['ch1'])
            line1.set_xdata(data['time'])
            plt.pause(0.0001)

except Exception as e:
    dl.stop_streaming()
    print(e)
finally:
    m.relinquish_ownership()





