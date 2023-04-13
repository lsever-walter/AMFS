import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

import numpy as _np
from PyQt5 import QtCore, QtGui, QtWidgets
from artiq.applets.simple import SimpleApplet
from jax import RealTimePlotApplet, JaxApplet


class PlotVoltageData(RealTimePlotApplet):
    def __init__(self, args, **kwds):
        num_of_traces = 1  
        datasets_names = ["voltage.trace_data"]
        xlabel = "Time (s)"
        ylabel = "Voltage (V)"
        super().__init__(num_of_traces, datasets_names, xlabel, ylabel, **kwds)

    def _set(self, dataset_name, value):
        if dataset_name == "voltage.trace_data":
            self._trace_data = value

    def _append(self, dataset_name, value):
        if dataset_name == "pmt.times":
            for kk in range(len(self.traces)):
                self.traces[kk].append_x(value)
        elif dataset_name == "pmt.counts_kHz":
            for kk in range(len(self.traces)):
                self.traces[0].append_y(value)
                self.traces[0].update_trace()  # only update the plot when counts are updated.


def main():
    applet = SimpleApplet(PlotVoltageData)
    PlotVoltageData.add_labrad_ip_argument(applet)
    applet.run()


if __name__ == "__main__":
    main()

