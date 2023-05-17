import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import integrate
from scipy.optimize import curve_fit

# Load the data from the CSV file
data0 = np.genfromtxt(r"C:\Users\wuhai\Downloads\test_circuit_1.csv", delimiter=',')
t0 = np.array(data0[:, 0])
v0 = np.array(data0[:, 1])

def pick_frame(t0, v0, f, r, sample_rate):
    #for f = 60 r =4
    #for f = 120-240, r=5
    #for f = 300, r=6
    frame = round(1/f, r)
    #cutoff number of points corresponding to period
    cutoff = int(1*frame*sample_rate)
    t0 = t0[0:cutoff]
    v0 = v0[0:cutoff]

    #center the data around zero so no DC offset
    v0 = v0-np.mean(v0)

    return t0, v0

def smooth_data(t, v, w):
    v_bin= v[:(v.size // w) * w].reshape(-1, w).mean(axis=1)
    t_bin= t[:(t.size // w) * w].reshape(-1, w).mean(axis=1)

    # t_bin = ((t + np.roll(t, 1))/2.0)[1::2]
    # v_bin = ((v + np.roll(v, 1))/2.0)[1::2]
    return t_bin, v_bin
    

def curve_fitter(t0, v0, omega, preset=False):
    if preset:
        def fitter_function(x, A, p):
            return  A*np.sin(2*np.pi*omega*x+p)
        
        opt, cov = curve_fit(fitter_function, t0, v0, p0=[.001, 0], maxfev=5000)

        print(opt[0])
        print(opt[1]/(2*np.pi))

    else:
        def fitter_function(x, A, w, p):
            return  A*np.sin(w*x+p)
    
        opt, cov = curve_fit(fitter_function, t0, v0, p0=[.001, 2*np.pi*omega, 0], maxfev=5000)

        print(opt[0])
        print(opt[1]/(2*np.pi))
        print(opt[2])
    
    
    return opt, cov

def plot_raw(t0, v0, plot):
    fig, ax = plt.subplots(1, 1, num=plot)
    
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
    #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Phase_Data/Raw/test_raw_300hz", dpi=300, transparent=False)


def plot_fitter(t0, v0,  opt, plot, omega, preset=False):
    fig, ax = plt.subplots(1, 1, num=plot)
    ax.plot(t0, v0, label="Raw")
    if preset:
        ax.plot(t0, opt[0]*np.sin(omega*t0 + opt[1]), label="Fitted")
    else:
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
    #plt.savefig("/Users/lseverwalter/code/AMFS/Controller/Phase_Data/Curve_Fit/test_fit_300hz", dpi=300, transparent=False)

t0b, v0b = smooth_data(t0, v0, 3)

t0b , v0b = pick_frame(t0b, v0b, 60, 4, 1e5/4)
t0, v0 = pick_frame(t0, v0, 60, 4, 1e5)


opt, cov = curve_fitter(t0, v0, 60)
optp, covp = curve_fitter(t0, v0, 60, True)


# optb, covb = curve_fitter(t0b, v0b, 60)

# plot_raw(t0, v0, 5)
# plot_raw(t0b, v0b, 6)

# plot_fitter(t0, v0, opt, 8, 60)


# plot_fitter(t0, v0, opt, 9, 60, preset=True)

