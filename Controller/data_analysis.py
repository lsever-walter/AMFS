import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = np.genfromtxt('/Users/lseverwalter/code/AMFS/Controller/Data/CSV/BField_Noise_3600_1.csv', delimiter=',')
# Split the columns into separate numpy arrays

t0 = np.array(data[:, 0])
v0 = np.array(data[:, 1])
# v1 = np.array(data[:, 2])


def absFFT(times,amplitude):
    fourierTransform = np.fft.fft(amplitude)/len(amplitude)
    fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    tpCount     = len(amplitude)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/samplingFrequency
    frequencies = values/timePeriod
    return frequencies, abs(fourierTransform)


def plotFourrier(t0, v0, t1=0, v1=0):
    freq0, fft0 = absFFT(t0,v0)
    
    freq0 = freq0[1:]
    fft0 = fft0[1:]

    fig, ax = plt.subplots(1, 1, num=3)
    ax.plot(freq0, fft0)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.set_xlim((min(freq0), 2500))
    ax.set_ylim((min(fft0)-.00005, .00005+max(fft0)))

    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_minor_locator(plt.MaxNLocator(25))
    #ax.xaxis.set_minor_locator(plt.FixedLocator(np.arange(ax.get_xlim()[0], ax.get_xlim()[1], 100)))

    # Add major and minor ticks to y-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_minor_locator(plt.MaxNLocator(25))
    #ax.yaxis.set_minor_locator(plt.FixedLocator(np.arange(ax.get_ylim()[0], ax.get_ylim()[1], .00005)))

    ax.tick_params(direction='in', top=True, right=True, which='both')

    #write code that adds major and minor ticks that are oriented inwards on all axes and that sets x and y limits adjusted for the maximum and minimum values for the y and x data
    plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Data/FFT_Plots/FFT_BField_Noise_5_1", dpi=300, transparent=False)
    plt.show()



def plot_data(t0, v0, t1=0, v1=0):
    fig, ax = plt.subplots(1, 1, num=2)
    ax.plot(t0, v0)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Voltage [V]")
    ax.set_xlim((-.25+min(t0), .25+max(t0)))
    ax.set_ylim((min(v0)-.005, .005+max(v0)))

    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_minor_locator(plt.MaxNLocator(25))
    #ax.xaxis.set_minor_locator(plt.FixedLocator(np.arange(ax.get_xlim()[0], ax.get_xlim()[1], .25)))

    # Add major and minor ticks to y-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_minor_locator(plt.MaxNLocator(15))
    #ax.yaxis.set_minor_locator(plt.FixedLocator(np.arange(ax.get_xlim()[0], ax.get_xlim()[1], .25)))

    ax.tick_params(direction='in', top=True, right=True, which='both')

    plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Data/Current_Plots/Coil_BField_5_1", dpi=300, transparent=False)
    plt.show()


def drift_quantify(v0):
    v_std = np.std(v0)
    v_rms = np.sqrt(np.mean(v0**2))

    return v_std, v_rms



# plot_data(t0, v0)
# plotFourrier(t0, v0)
std, rms = drift_quantify(v0)
print(std, rms)

