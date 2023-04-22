import numpy as np
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = np.genfromtxt('/Users/lseverwalter/code/AMFS/Controller/Data/CSV/Coil_Noise_Data_30_1.csv', delimiter=',')

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
    
    freq0 = np.delete(freq0, 0)
    fft0 = np.delete(fft0, 0)

    plt.figure(3)
    plt.plot(freq0, fft0)
    plt.xlabel("frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Data/FFT_Plots/FFT_Coil_Noise_30_1", dpi=300, transparent=False)
    plt.show()



def plot_data(t0, v0, t1=0, v1=0):
    plt.plot(t0, v0)
    plt.title("Current Noise Data")
    plt.xlabel("Seconds")
    plt.ylabel("Volts")
    plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Data/Current_Plots/Coil_Noise_30_1", dpi=300, transparent=False)
    plt.show()


plot_data(t0, v0)
plotFourrier(t0, v0)

