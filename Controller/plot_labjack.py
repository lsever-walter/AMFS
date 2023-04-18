import sys
import traceback
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import u3


class LabjackPlotter():
    def __init__(self) -> None:
        self.u3 = u3.U3()

    def close(self):
        self.u3.close()
        

    def absFFT(self,times,amplitude):
        fourierTransform = np.fft.fft(amplitude, norm="backward")/len(amplitude)
        fourierTransform = fourierTransform[range(int(len(amplitude)/2))]
        
        samplingFrequency = 1/((times[-1]-times[0])/len(times))
        
        tpCount     = len(amplitude)

        values      = np.arange(int(tpCount/2))

        timePeriod  = tpCount/samplingFrequency

        frequencies = values/timePeriod


        return frequencies, abs(fourierTransform)


    def get_channel(self, whichChannel = "AIN0"):

        # MAX_REQUESTS is the number of packets to be read.
        MAX_REQUESTS = 5
        # SCAN_FREQUENCY is the scan frequency of stream mode in Hz
        SCAN_FREQUENCY = 5000
        # To learn the if the U3 is an HV

        # Set the FIO0 and FIO1 to Analog (d3 = b00000011)
        #d.configIO(FIOAnalog=3,NumberOfTimersEnabled = 2) #don't call this if you've set up PWM to do something you care about.
        #print("Configuring U3 stream")
        self.u3.streamConfig(NumChannels=2, PChannels=[0, 1], NChannels=[31, 31], Resolution=3, ScanFrequency=SCAN_FREQUENCY)

        #d.streamStop() #this is not strictly necessary but makes things more robust; without it it crashes if a steam has already been started

        print("Start stream")
        try:
            self.u3.streamStart()
        except:
            print("Stopping existing stream..")
            self.u3.streamStop()
            time.sleep(0.1)
            self.u3.streamStart()
            
        start = datetime.now()
        print("Start time is %s" % start)

        missed = 0
        dataCount = 0
        packetCount = 0

        allSamples = np.array([])
        for r in self.u3.streamData():
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
        self.u3.streamStop()
        print("Stream stopped.\n")

        return time_list, allSamples



    def plotChannel(self, whichChannel = "AIN0" ):
        times, voltages = self.get_channel(whichChannel)
        plt.figure()
        plt.plot(times ,voltages, 'b-', label=whichChannel)
        plt.xlabel("Time (s)")
        plt.ylabel("Volts (V)")
        plt.title(f"{whichChannel}")
    

    def get_two_channels(self):
        # MAX_REQUESTS is the number of packets to be read.
        MAX_REQUESTS = 5
        # SCAN_FREQUENCY is the scan frequency of stream mode in Hz
        SCAN_FREQUENCY = 5000
    
        # To learn the if the U3 is an HV

        # Set the FIO0 and FIO1 to Analog (d3 = b00000011)
        #d.configIO(FIOAnalog=3,NumberOfTimersEnabled = 2) #don't call this if you've set up PWM to do something you care about.
        #print("Configuring U3 stream")
        self.u3.streamConfig(NumChannels=2, PChannels=[0, 1], NChannels=[31, 31], Resolution=3, ScanFrequency=SCAN_FREQUENCY)

        #d.streamStop() #this is not strictly necessary but makes things more robust; without it it crashes if a steam has already been started
    
        print("Start stream")
        try:
            self.u3.streamStart()
        except:
            print("Stopping existing stream..")
            self.u3.streamStop()
            time.sleep(0.1)
            self.u3.streamStart()
            
        start = datetime.now()
        print("Start time is %s" % start)

        missed = 0
        dataCount = 0
        packetCount = 0

        allSamples0 = np.array([])
        allSamples1 = np.array([])
        for r in self.u3.streamData():
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
        self.u3.streamStop()
        
        print("Stream stopped.\n")
    
        
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
    
    
    def plotFourrier(self):
        t0, d0, t1, d1 = self.plotTwoChannels()
        
        freq0, FFT0 = self.absFFT(t0,d0)
        freq1, FFT1 = self.absFFT(t1,d1)
        
        plt.figure(3)
        plt.plot(freq0, FFT0)
        plt.xlabel("Frequency [Hz]")
        plt.title("Output (AIN0) FFT")
        
        
        plt.figure(4)
        plt.plot(freq1, FFT1)
        plt.xlabel("Frequency [Hz]")
        plt.title("Input (AIN1) FFT")