import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import integrate
from scipy.optimize import curve_fit

# Load the data from the CSV file
data0 = np.genfromtxt('/Users/lseverwalter/code/AMFS/Controller/Phase_Data/CSV/test_circuit_1.csv', delimiter=',')
t0 = np.array(data0[:, 0])
v0 = np.array(data0[:, 1])

#set sample rate
sample_rate = 1e5


#choose which period we want to fit using
frame1 = round(1/60, 4)

frame2 = round(1/120, 5)

frame3 = round(1/180, 5)

frame4 = round(1/240, 5)

frame5 = round(1/300, 6)

#cutoff number of points corresponding to period
cutoff = int(1*frame5*sample_rate)
t0 = t0[0:cutoff]
v0 = v0[0:cutoff]

#center the data around zero so no DC offset
v0 = v0-np.mean(v0)


def curve_fitter(t0, v0, omega):
    def fitter_function(x, A, w, p):
        return  A*np.sin(w*x+p)
    
    opt, cov = curve_fit(fitter_function, t0, v0, p0=[.001, 2*np.pi*omega, 0], maxfev=5000)
    print(opt[0])
    print(opt[1]/(2*np.pi))
    print(opt[2])


    return opt, cov

def plot_raw(t0, v0):
    fig, ax = plt.subplots(1, 1, num=1)
    
    ax.plot(t0, v0, label="Raw")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("Voltage [V]")

    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Phase_Data/Raw/test_raw_300hz", dpi=300, transparent=False)



def plot_fitter(t0, v0,  opt):
    fig, ax = plt.subplots(1, 1, num=2)
    ax.plot(t0, v0, label="Raw")
    ax.plot(t0, opt[0]*np.sin(opt[1]*t0 + opt[2]), label="Fitted")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("Voltage [V]")

    ax.legend(loc='upper left', fontsize=16)
    ax.tick_params(axis='both', which='both', direction='in',
                        top=True, right=True, labelsize=16)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_size(20)
    plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Phase_Data/Curve_Fit/test_fit_300hz", dpi=300, transparent=False)

opt, cov = curve_fitter(t0, v0, 300)
plot_raw(t0, v0)
plot_fitter(t0, v0, opt)
