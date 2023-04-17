#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 17:12:15 2023

@author: lseverwalter
"""

import sys
import traceback
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import u3


def absFFT(times,amplitude):
    fourierTransform = np.fft.fft(amplitude, norm="backward")/len(amplitude)
    fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
    
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    
    tpCount     = len(amplitude)

    values      = np.arange(int(tpCount/2))

    timePeriod  = tpCount/samplingFrequency

    frequencies = values/timePeriod


    return frequencies, abs(fourierTransform)

def testFourier():
    times = np.linspace(0,10,2000)
    f1 = 12  #in Hertz
    f2 = 20  #in Hertz
    testFunction = np.cos(times * f1 * 2 * np.pi) + (2*np.sin(times * f2 * 2 * np.pi))
    frequencies,powerSpectrum = absFFT(times,testFunction)
    
    plt.figure()
    plt.subplot(211)
    plt.plot(times,testFunction, 'g-', label='test Function')
    plt.xlabel('time, seconds')
    plt.legend()
    
    plt.subplot(212)
    plt.plot(frequencies,powerSpectrum, 'b-',label='fourier transform. Should have peaks at 12 and 20')
    plt.xlabel('frequency, Hz')
    plt.legend()
    


    
def getFourierComponentFastFFT(times,data,f):
    fourierTransform = np.fft.fft(data, norm="backward")/len(data)
    fourierTransform = fourierTransform[range(int(len(data)/2))]
    
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    
    tpCount     = len(data)

    values      = np.arange(int(tpCount/2))

    timePeriod  = tpCount/samplingFrequency

    frequencies = values/timePeriod
    
    return 2*(fourierTransform[f]).imag , 2*(fourierTransform[f]).real


def getFourierComponent(times,data,f=-1):
    N = len(times)
    n = np.arange(N)
    k = n.reshape((N, 1))
    exp = np.exp(-2j * np.pi * n * k/N)
    
    Spectrum = np.dot(exp, data)
    
    if f>=0:
        
        return 2*Spectrum[f].imag/N, 2*Spectrum[f].real/N
    
    else:
        
        return 2*Spectrum
        

def overlayFourier():
    times = np.linspace(0,1,2000)
    f1 = 12  #in Hertz
    f2 = 20  #in Hertz
    testFunction = np.cos(times * f1 * 2 * np.pi) + (2*np.sin((times * f2 * 2 * np.pi) + 1))
    frequencies,powerSpectrum = absFFT(times,testFunction)
    
    f = 20 
    sinAmp,cosAmp = getFourierComponent(times,testFunction,f)
    fitData = sinAmp * np.sin(f * 2 * np.pi * times) + cosAmp * np.cos(f * 2 * np.pi * times)

    plt.figure()
    plt.plot(times,testFunction, 'b-', label='test Function')
    plt.plot(times,fitData, 'g-', label='best fit at %d Hz'%f)
    plt.xlabel('time, seconds')
    plt.legend()
    




def absSlowFT(times,data):
    
    Spectrum = getFourierComponent(times, data) 
    Spectrum = np.array(Spectrum)
    Spectrum = Spectrum[range(int(len(data)/2))]
    

    samplingFrequency = 1./((times[-1]-times[0])/len(times))
    tpCount     = len(data)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/samplingFrequency
    frequencies = values/timePeriod

    
    return frequencies, abs(Spectrum)



def testFourierBoth():
    times = np.linspace(0,10,2000)
    f1 = 12  #in Hertz
    f2 = 20  #in Hertz
    testFunction = np.cos(times * f1 * 2 * np.pi) + (2*np.sin(times * f2 * 2 * np.pi))
    frequencies , powerSpectrum = absSlowFT(times,testFunction)
    
    frequencies_fast, powerSpectrumFast = absFFT(times,testFunction)
    
    plt.figure()
    plt.subplot(211)
    plt.plot(times,testFunction, 'g-', label='test Function')
    plt.xlabel('time, seconds')
    plt.legend()
    
    plt.subplot(212)
    plt.plot(frequencies,powerSpectrum, 'b-',label='slow')
    plt.plot(frequencies_fast, powerSpectrumFast, label="fast")
    plt.xlabel('frequency, Hz')
    plt.title("Slow FT")
    plt.legend()
    



def get_channel(whichChannel = "AIN0"):
    # MAX_REQUESTS is the number of packets to be read.
    MAX_REQUESTS = 5
    # SCAN_FREQUENCY is the scan frequency of stream mode in Hz
    SCAN_FREQUENCY = 5000
   
    d = u3.U3()
    # To learn the if the U3 is an HV

    # Set the FIO0 and FIO1 to Analog (d3 = b00000011)
    #d.configIO(FIOAnalog=3,NumberOfTimersEnabled = 2) #don't call this if you've set up PWM to do something you care about.
    #print("Configuring U3 stream")
    d.streamConfig(NumChannels=2, PChannels=[0, 1], NChannels=[31, 31], Resolution=3, ScanFrequency=SCAN_FREQUENCY)

    #d.streamStop() #this is not strictly necessary but makes things more robust; without it it crashes if a steam has already been started
   
    print("Start stream")
    try:
        d.streamStart()
    except:
        print("Stopping existing stream..")
        d.streamStop()
        time.sleep(0.1)
        d.streamStart()
        
    start = datetime.now()
    print("Start time is %s" % start)

    missed = 0
    dataCount = 0
    packetCount = 0

    allSamples = np.array([])
    for r in d.streamData():
        if r is not None:
            # Our stop condition
            if dataCount >= MAX_REQUESTS:
                break


            # Comment out these prints and do something with r
            #print("Average of %s AIN0, %s AIN1 readings: %s, %s" %
            #      (len(r["AIN0"]), len(r["AIN1"]), sum(r["AIN0"])/len(r["AIN0"]), sum(r["AIN1"])/len(r["AIN1"])))
            allSamples = np.concatenate((allSamples,r[whichChannel]))
            dataCount += 1
            #packetCount += r['numPackets']
        else:
            # Got no data back from our read.
            # This only happens if your stream isn't faster than the USB read
            # timeout, ~1 sec.
            print("No data ; %s" % datetime.now())
    
    
    stop = datetime.now()
    time = (stop-start).total_seconds()
    time_list = np.linspace(0, time, len(allSamples))
    d.streamStop()
    print("Stream stopped.\n")
    d.close()
    
    return time_list, allSamples



def plotChannel(whichChannel = "AIN0" ):
    times, voltages = get_channel(whichChannel)
    plt.figure()
    plt.plot(times ,voltages, 'b-', label=whichChannel)
    plt.xlabel("Time (s)")
    plt.ylabel("Volts (V)")
    plt.title(f"{whichChannel}")
    




def absFFT(times,amplitude):
    fourierTransform = np.fft.fft(amplitude)/len(amplitude)
    fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
    
    samplingFrequency = 1/((times[-1]-times[0])/len(times))
    
    tpCount     = len(amplitude)

    values      = np.arange(int(tpCount/2))

    timePeriod  = tpCount/samplingFrequency

    frequencies = values/timePeriod


    return frequencies, abs(fourierTransform)


            
class PWM():
    def __init__(self):
        self.labjack = u3.U3()
        self.labjack.configIO(NumberOfTimersEnabled = 2,FIOAnalog=3)
        self.labjack.configTimerClock(TimerClockBase = 6, TimerClockDivisor = 3)
        
    def close(self):
        self.labjack.close()
        
    def setPWM(self, highFraction, whichTimer):
        
        i = 65535-int(65535*highFraction)
        if (highFraction <= 1) and (highFraction >=0):
            if whichTimer == 0:
                self.labjack.getFeedback(self.config.Timer0Config(TimerMode = 0, Value = i))
            else:
                self.labjack.getFeedback(self.config.Timer1Config(TimerMode = 1, Value = i))
        else:
            print("Sorry, fraction must be between 0 and 1")
        
      

        
def plotTwoChannels():
    # MAX_REQUESTS is the number of packets to be read.
    MAX_REQUESTS = 5
    # SCAN_FREQUENCY is the scan frequency of stream mode in Hz
    SCAN_FREQUENCY = 5000
   
    d = u3.U3()
    # To learn the if the U3 is an HV

    # Set the FIO0 and FIO1 to Analog (d3 = b00000011)
    #d.configIO(FIOAnalog=3,NumberOfTimersEnabled = 2) #don't call this if you've set up PWM to do something you care about.
    #print("Configuring U3 stream")
    d.streamConfig(NumChannels=2, PChannels=[0, 1], NChannels=[31, 31], Resolution=3, ScanFrequency=SCAN_FREQUENCY)
    
    
    
    
    #d.streamStop() #this is not strictly necessary but makes things more robust; without it it crashes if a steam has already been started
   
    print("Start stream")
    try:
        d.streamStart()
    except:
        print("Stopping existing stream..")
        d.streamStop()
        time.sleep(0.1)
        d.streamStart()
        
    start = datetime.now()
    print("Start time is %s" % start)

    missed = 0
    dataCount = 0
    packetCount = 0

    allSamples0 = np.array([])
    allSamples1 = np.array([])
    for r in d.streamData():
        if r is not None:
            # Our stop condition
            if dataCount >= MAX_REQUESTS:
                break


            # Comment out these prints and do something with r
            #print("Average of %s AIN0, %s AIN1 readings: %s, %s" %
            #      (len(r["AIN0"]), len(r["AIN1"]), sum(r["AIN0"])/len(r["AIN0"]), sum(r["AIN1"])/len(r["AIN1"])))
            allSamples0 = np.concatenate((allSamples0,r["AIN0"]))
            allSamples1 = np.concatenate((allSamples1,r["AIN1"]))
            dataCount += 1
            #packetCount += r['numPackets']
        else:
            # Got no data back from our read.
            # This only happens if your stream isn't faster than the USB read
            # timeout, ~1 sec.
            print("No data ; %s" % datetime.now())
    
    
    stop = datetime.now()
    time = (stop-start).total_seconds()
    time_list_0 = np.linspace(0, time, len(allSamples0))
    time_list_1 = np.linspace(0, time, len(allSamples1))
    d.streamStop()
    
    print("Stream stopped.\n")
    d.close()
   
    
    plt.figure(1)
    plt.plot(time_list_0,allSamples0, 'b-', label="AIN0")
    plt.xlabel("Time (s)")
    plt.ylabel("Volts (V)")
    plt.title("AIN0")
    plt.legend()
    
    plt.figure(2)
    plt.plot(time_list_1,allSamples1, 'b-', label="AIN1")
    plt.xlabel("Time (s)")
    plt.ylabel("Volts (V)")
    plt.title("AIN1")
    plt.legend()
    
    return time_list_0, allSamples0, time_list_1, allSamples1
    

    
def plotFourrier():
    t0, d0, t1, d1 = plotTwoChannels()
    
    freq0, FFT0 = absFFT(t0,d0)
    freq1, FFT1 = absFFT(t1,d1)
    
    plt.figure(3)
    plt.plot(freq0, FFT0)
    plt.xlabel("Frequency [Hz]")
    plt.title("Output (AIN0) FFT")
    
    
    plt.figure(4)
    plt.plot(freq1, FFT1)
    plt.xlabel("Frequency [Hz]")
    plt.title("Input (AIN1) FFT")
    
 

# testFourier()
# overlayFourier()
# testFourierBoth()

    
# pwm = PWM()
# pwm.setPWM(0, 0)
# pwm.close()

# plotChannel("AIN0")
# plotChannel("AIN1")

# plotFourrier()