import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import integrate

# Load the data from the CSV file
data1 = np.genfromtxt('File1', delimiter=',')
data0 = np.genfromtxt('File2', delimiter=',')
# Split the columns into separate numpy arrays

#save data to different arrays for different files
t0 = np.array(data0[:, 0])
v0 = np.array(data0[:, 1])
# v01 = np.array(data0[:, 2])

t1 = np.array(data1[:, 0])
v1 = np.array(data1[:, 1])
v11 = np.array(data1[:, 2])



def absFFT(times,amplitude):
    '''Function to preform a fast fourier transform on voltage vs time data from the magnetic field'''
    fourierTransform = np.fft.fft(amplitude)/len(amplitude)
    fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    tpCount     = len(amplitude)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/samplingFrequency
    frequencies = values/timePeriod
    return frequencies, abs(fourierTransform)

def drift_quantify(v0):
    '''return the standard deviation and root mean square value of the magnetic field'''
    v_std = np.std(v0)
    v_rms = np.sqrt(np.mean(v0**2))
    print(f"The standard deviation is: {v_rms}")
    print(f"The rms is: {v_rms}")
    return v_std, v_rms


def integrator(t, v):
    '''integrate under the powerspectrum vs frequency graph to determine noise reduction'''
    freq, fft = absFFT(t,v)
    freq = freq[0:1000]
    fft= fft[0:1000]
    area_simpson = integrate.simps(y=fft, x=freq)
    return round(area_simpson, 6)

def plot_data(t, v):
    '''plot and save raw data to a csv file'''
    fig, ax = plt.subplots(1, 1, num=3)
    ax.plot(t, v)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Voltage [V]")
    ax.set_xlim((-.25+min(t), .25+max(t)))
    ax.set_ylim((min(v)-.005, .005+max(v)))

    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    
    #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Filter_Test/Raw_Plot/lowpass_filter_test_raw_1", dpi=300, transparent=False)
    plt.show()


def plotFourrier(t, v, log=False):
    '''plot fourrier transform, can choose to plot loglog. WARNING: the loglog code should be updated to make sure the units are in dBG/sqrt(Hz), can be done with scipy'''
    freq, fft = absFFT(t,v)
    
    area = round(integrator(t, v), 6)

    freq = freq[1:]
    fft = fft[1:]

    fig, ax = plt.subplots(1, 1, num=1)
    ax.plot(freq, fft, label=f"Area= {area}")
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.set_xlim((min(freq), 1000))
    ax.set_ylim((min(fft)-(4e-6), .00005+max(fft)))

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
        ax.set(xlabel='Log(Frequency)', xlim=None)
        ax.set(ylabel='Log(Power)', ylim=None)
        
        
        
        #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Filter_Test/FFT/lowpass_filter_test_ll_1", dpi=300, transparent=False)

    elif not log:
        #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Filter_Test/FFT/lowpass_filter_test_1", dpi=300, transparent=False)
        pass
    
    
    plt.show()


def overplot_fourrier(t0, v0, t1, v1, log=False):
    '''plot fourrier transform of two data sets over each other,
    can choose to plot loglog. 
    WARNING: the loglog code should be updated to make sure the units are in dBG/sqrt(Hz), can be done with scipy'''
    freq0, fft0 = absFFT(t0,v0)
    freq1, fft1 = absFFT(t1, v1)

    area0 = round(integrator(t0, v0), 6)
    area1 = round(integrator(t1, v1), 6)

    freq0 = freq0[2:]
    fft0 = fft0[2:]
    
    freq1 = freq1[2:]
    fft1 = fft1[2:]


    if log:
        fft0 = 20 * np.log10(fft0)
        fft1 = 20 * np.log10(fft1)
        # freq0 = np.sqrt(freq0)
        # freq1 = np.sqrt(freq1)

    fig, ax = plt.subplots(1, 1, num=2)
    ax.plot(freq0, fft0, label=f"PID ON Raw(A={area0})")
    ax.plot(freq1, fft1, label=f"PID OFF Raw(A={area1})")
    
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.set_title("PID ON vs. OFF")
    
    ax.set_xlim((min(freq0)-30, 1000))
    ax.set_ylim((min(fft0)-(4e-6), .00005+max(fft0)))

    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)

    if log:
        ax.set_xscale('log')
        #ax.set_yscale('log')
        ax.set(xlabel='frequency [Hz]', xlim=None)
        ax.set(ylabel='Power (dB)', ylim=(-160, -40))
        
    elif not log:
        pass
   
    #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Filter_Test/FFT_Overplot/lowpass_filter_test_1", dpi=300, transparent=False)
    plt.show()





# plot_data(t0, v0)
# plot_data(t1, v1)

# plot_data(t0, v01)
# plot_data(t1, v11)


# plotFourrier(t0, v0, log=True)
# plotFourrier(t0, v01, log=True)
# plotFourrier(t1, v11, log=True)
#overplot_fourrier(t0, v0, t1, v1, log=True)

# af = integrator(t1, v1)
# anf = integrator(t0, v0)
# ratio = af/anf

# print(f"This is no filter {anf}")
# print(f"This is with filter {af}")
# print(f"no filter/filter: {ratio}")