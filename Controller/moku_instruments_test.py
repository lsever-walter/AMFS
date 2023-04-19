from moku.instruments import MultiInstrument
from moku.instruments import Datalogger, Oscilloscope, PIDController
import matplotlib.ticker as tck
import matplotlib as plt


class Moku_Go:
    def __init__(self, moku_ip):
        self.moku = MultiInstrument(moku_ip, platform_id=2,
                                    force_connect=True)
        try:
            self.pid = self.moku.set_instrument(1, PIDController)
            self.osc = self.moku.set_instrument(2, Oscilloscope)

            #print(self.moku.set_connections(connections=connections))
        except Exception as e:
            print(f"Unable to connect to Moku: {e}")

    def moku_power_supply(self, unit, vol, amp):
        """ Enable Moku Go's power supplies instrument.
        Params:
        unit (int): the id number of the power supply you are using
        vol (float): output voltage in Volt (-5 V < vol < 5 V)
        amp (float): output current in Amperes (0 < amp < 0.15 A)
        """
        try:
            self.moku.set_power_supply(unit, enable=True,
                                       voltage=vol, current=amp)
            print(self.moku.get_power_supply(unit))
        except Exception as e:
            print(f"Failed to enable the power supply instrument: {e}")


    def real_time_plotting(self): # needs to be tuned!!!
        fig, ax = plt.subplots()
        line1, = ax.plot([], [], label='ch1')
        line2, = ax.plot([], [], label='ch2')

        data = self.pid.get_data()  # Initial Frame
        x_min, x_max = data['time'][0], data['time'][-1]  # Assuming the axis is not changing
        ax.set_xlim(x_min, x_max)
        ax.tick_params(axis='both', which='both', direction='in',
                          top=True, right=True)
        ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        ax.yaxis.set_minor_locator(tck.AutoMinorLocator())

        #while True:
           # data = to be continued

    def moku_close(self):
        """ Close the connection to the Moku device, this ensurs network
        resources and released correctly."""
        self.moku.relinquish_ownership()


def main():
    moku_ip = r'[fe80:0000:0000:0000:7269:79ff:feb9:3e1e%20]'
    my_moku = Moku_Go(moku_ip)


if __name__ == "__main__":
    main()
