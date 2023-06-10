import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import integrate, signal

# Load different data different the CSV files
data1 = np.genfromtxt('', delimiter=',')
data0 = np.genfromtxt('', delimiter=',')

# Split the columns into separate numpy arrays
#save data to different arrays for different files
t0 = np.array(data0[:, 0])
v0 = np.array(data0[:, 1])
# v01 = np.array(data0[:, 2])

t1 = np.array(data1[:, 0])
v1 = np.array(data1[:, 1])
v11 = np.array(data1[:, 2])



def absFFT(times,amplitude):
    '''Perfoms discrete fast fourier transform on voltage-time series data
    Input:
        times: numpy array of time data
        amplitude: numpy array of voltage data
    Return:
        frequencies: numpy array of fft frequency
        abs(fourierTransform): numpy array of absolute value of fourier spectrum
    '''
    fourierTransform = np.fft.fft(amplitude)/len(amplitude)
    fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    tpCount     = len(amplitude)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/samplingFrequency
    frequencies = values/timePeriod
    return frequencies, abs(fourierTransform)

def drift_quantify(v0):
    '''return the standard deviation and root mean square value of the input numpy array'''
    v_std = np.std(v0)
    v_rms = np.sqrt(np.mean(v0**2))
    print(f"The standard deviation is: {v_rms}")
    print(f"The rms is: {v_rms}")
    return v_std, v_rms


def integrator(x,y):
    '''numerical integration with adjustable limits on integrated frequencies (x)'''
    y=y[0:1000]
    x=x[0:1000]

    area_simpson = integrate.simps(y, x)
    return round(area_simpson, 10)

def plot_data(t, v):
    '''
    Function to plot raw voltage-time series data and save it to a .csv file in a subdirectory
    '''
    
    #setup plot
    fig, ax = plt.subplots(1, 1, num=3)
    ax.plot(t, v)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Voltage [V]")
    ax.set_xlim((-.25+min(t), .25+max(t)))
    ax.set_ylim((min(v)-.005, .005+max(v)))

    #setup axes
    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    
    plt.savefig("", dpi=300, transparent=False)
    plt.show()


def plotFourrier(t, v, scaling):
    '''
    Can choose between plotting the:
        1. discete fast fourier transform of the voltage vs. time data
        2. the power spectral density of the voltage vs. time data
        3. the power spectral density of the voltage vs. time data in dBG/sqrt(Hz) vs. Hz units

    Input:
        t: numpy array of time series
        v: numpy array of voltage series
        scaling: str, set the axes and scaling of data
    '''

    #setup plot
    fig, ax = plt.subplots(1, 1, num=1)


    if scaling=="log_psd":
        #scale power spectral density to dBG^2/Hz

        #find the psd using the scipy.signal.periodogram function
        freq0, fft0 = signal.periodogram(v, 3000, scaling="density")
        
        #find the area under the spectral curve
        area0 = integrator(freq0, fft0)
        
        #convert to dBG^2/Hz
        fft0 = 10*np.log(fft0)
       
        #set axes for plot
        ax.set(xlabel='frequency [Hz]', xlim=(.1, 3e3))
        ax.set(ylabel='Power (dB)', ylim=(-400, -100))
        ax.set_xscale("log")
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("Power Spectral Density [dBG^2/Hz]")

    elif scaling == "psd":
        #plot just the power spectral density as G^2/Hz

        #find the psd using the scipy.signal.periodogram function
        freq0, fft0 = signal.periodogram(v, 3000, scaling="density")
        
        #find the area under the spectral curve
        area0 = integrator(freq0, fft0)
        
        #set axes for plot
        ax.set(xlabel='frequency [Hz]', xlim=(.1, 10))
        ax.set(ylabel='Power (dB)', ylim=(0,1e-7))
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("PSD")
    
    else:
        #plot the discrete FFT
        freq0, fft0 = absFFT(t0,v0)
        area0 = integrator(freq0, fft0)
        
        #set range of data plotted
        freq0 = freq0[2:]
        fft0 = fft0[2:]
        freq1 = freq1[2:]
        fft1 = fft1[2:]

        #set axes for plot
        ax.set_xlim((min(freq0)-30, 1000))
        ax.set_ylim((min(fft0)-(4e-6), .00005+max(fft0)))
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("Amplitude [G]")


    #plot series, setup legend and axes ticks
    ax.plot(freq0, fft0, label=f"PID ON Raw(A={area0})")
    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)    
    
    #save figure in csv format, can add subdirectory, filename, etc...
    plt.savefig(f"/{scaling}", dpi=300, transparent=False)
    
    plt.show()


def overplot_fourrier(t0, v0, t1, v1, scaling):
    '''
    Can choose between plotting the two data sets on top of each other as:
        1. discete fast fourier transform of the voltage vs. time data
        2. the power spectral density of the voltage vs. time data
        3. the power spectral density of the voltage vs. time data in dBG/sqrt(Hz) vs. Hz units

    Input:
        t0, t1: numpy array of time series for each data set
        v0, v1: numpy array of voltage series for each data set
        scaling: str, set the axes and scaling of data
    '''
    
    
    fig, ax = plt.subplots(1, 1, num=2)

    if scaling=="log_psd":
        #scale power spectral density to dBG^2/Hz vs. Hz

        #find the psd using the scipy.signal.periodogram function
        freq0, fft0 = signal.periodogram(v0, 3000, scaling="density")
        freq1, fft1 = signal.periodogram(v1, 3000, scaling="density")
        
        #find the areas under the spectral density curve
        area0 = integrator(freq0, fft0)
        area1 = integrator(freq1, fft1)
        
        #convert to dBG^2/Hz
        fft0 = 10*np.log(fft0)
        fft1 = 10*np.log(fft1)
        
        #set axes for plot
        ax.set(xlabel='frequency [Hz]', xlim=(.1, 3e3))
        ax.set(ylabel='Power (dB)', ylim=(-400, -100))
        ax.set_xscale("log")
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("Power Spectral Density [dBG^2/Hz]")

    elif scaling == "psd":
        #plot power spectral density as G^2/Hz vs Hz
        
        #find the psd using the scipy.signal.periodogram function
        freq0, fft0 = signal.periodogram(v0, 3000, scaling="density")
        freq1, fft1 = signal.periodogram(v1, 3000, scaling="density")
        
        #find the areas under the spectral density curve
        area0 = round(integrator(freq0, fft0), 6)
        area1 = round(integrator(freq1, fft1), 6)

        #set the axes for plot
        ax.set(xlabel='frequency [Hz]', xlim=(0, 300))
        ax.set(ylabel='Power (dB)', ylim=(0,.000001))
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("PSD")
    
    else:
        #plot discete FFT of v vs. frequency
        
        #find the fft of the voltage time data
        freq0, fft0 = absFFT(t0,v0)
        freq1, fft1 = absFFT(t1, v1)
        
        #find the area under the FFT curve
        area0 = integrator(freq0, fft0)
        area1 = integrator(freq1, fft1)
        
        #change the range of data plotted (can eliminate DC signal from plot)
        freq0 = freq0[2:]
        fft0 = fft0[2:]
        freq1 = freq1[2:]
        fft1 = fft1[2:]

        #set axes
        ax.set_xlim((min(freq0)-30, 1000))
        ax.set_ylim((min(fft0)-(4e-6), .00005+max(fft0)))
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("Amplitude [G]")


    #plot series
    ax.plot(freq0, fft0, label=f"PID ON Raw(A={area0})")
    ax.plot(freq1, fft1, label=f"PID OFF Raw(A={area1})")
    
    #set title
    ax.set_title("PID ON vs. OFF")
    
    #set legend and axes
    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)

    #save figure
    plt.savefig(f"/{scaling}", dpi=300, transparent=False)
    plt.show()


#call functions to generate plots
plot_data(t0, v0)
plot_data(t1, v1)
plotFourrier(t0, v0, scaling="log_psd")
plotFourrier(t1, v1, scaling="psd")
overplot_fourrier(t0, v0, t1, v1, scaling="log_psd")






