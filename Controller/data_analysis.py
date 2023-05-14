import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import integrate

# Load the data from the CSV file
data = np.genfromtxt('/Users/lseverwalter/code/AMFS/Controller/Data/Active_Filter/no_filter_voltage.csv', delimiter=',')
# Split the columns into separate numpy arrays

t0 = np.array(data[:, 0])
v0 = np.array(data[:, 1])
v1 = np.array(data[:, 2])


def absFFT(times,amplitude):
    fourierTransform = np.fft.fft(amplitude)/len(amplitude)
    fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    tpCount     = len(amplitude)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/samplingFrequency
    frequencies = values/timePeriod
    return frequencies, abs(fourierTransform)


def plotFourrier(t0, v0, t1=0, v1=0, log=False):
    freq0, fft0 = absFFT(t0,v0)
    
    area = noise_quantify(t0, v0)

    freq0 = freq0[1:]
    fft0 = fft0[1:]

    fig, ax = plt.subplots(1, 1, num=3)
    ax.plot(freq0, fft0)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.set_xlim((min(freq0), 500))
    ax.set_ylim((min(fft0)-.00005, .00005+max(fft0)))

    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)

    if log:
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set(xlabel='Log(Frequency)')
        ax.set(ylabel='Log(Power)', ylim=(5e-9, 1))

    elif not log:
        pass

    #write code that adds major and minor ticks that are oriented inwards on all axes and that sets x and y limits adjusted for the maximum and minimum values for the y and x data
    #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Data/Active_Filter/active_filter_voltage_7", dpi=300, transparent=False)
    plt.show()



def plot_data(t0, v0, t1=0, v1=0):
    fig, ax = plt.subplots(1, 1, num=2)
    ax.plot(t0, v0)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Voltage [V]")
    ax.set_xlim((-.25+min(t0), .25+max(t0)))
    ax.set_ylim((min(v0)-.005, .005+max(v0)))

    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    
    # plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Data/Active_Filter/active_filter_voltage_7", dpi=300, transparent=False)
    plt.show()


def drift_quantify(v0):
    v_std = np.std(v0)
    v_rms = np.sqrt(np.mean(v0**2))
    print(f"The standard deviation is: {v_rms}")
    print(f"The rms is: {v_rms}")
    return v_std, v_rms


def noise_quantify(t0, v0):
    freq0, fft0 = absFFT(t0,v0)
    area_simpson = integrate.simpson(y=fft0, x=freq0)
    return area_simpson,



plot_data(t0, v0)
plotFourrier(t0, v0, log=True)
# std, rms = drift_quantify(v0)
noise_quantify(t0, v0)



