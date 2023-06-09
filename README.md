# Active Magnetic Field Stabilization
Our goal is to generate magnetic fields on the order of 3 Gauss and to stabilize these magnetic fields to within a signal-noise ratio of 1e3 for longterm drift (over the course of hours to days) and for 60Hz harmonic noise. This magnetic field stabilization scheme will improve stability for experiments that rely on (near) constant magnetic fields.

## Table of Contents
- [Motivation](#Motivation)
  - [Zeeman Sublevels and Fine Structure](#Zeeman-Sublevels-and-Fine-Structure)
  - [Zeeman Effect](#The-Zeeman-Effect)
- [Components](#Components)
- [Schematic](#Schematic)
  - [Experimental Setup](#Experimental-Setup)
  - [Moku Go](#Moku-Go)
  - [N Channel MOSFET](#N-Channel-Mosfet)
  - [Helmholtz Coils](#Helmholtz-Coils)
  - [Magnetometer](#Magnetometer)
- [Feedback Control](#Feedback-Control)
  - [PID Controller](#PID-Controller-(Moku-Go))
  - [Tuning Controller](#Tuning-Controller)
- [Feedforward Control](#Feedforward-Control)
  - [Line Triggering](#Line-Triggering)
  - [60Hz Harmonic Cancellation](#60Hz-Harmonic-Cancellation)
- [Combined Feedback Feedforward Control](#Feedback-and-Feedforward)
- [Future Work](#Future-Work)
  

  
  



# Motivation

## Zeeman Sublevels and Fine Structure
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/ef402b0fd69e2dcd81f24fc7162477f2025e19df/Figures/Sr87%2B_level_diagram.png" width="1000">
</div>

In many physics groups investigating the interaction between light and matter use single, or few, atoms confined to a "trapping region." Lasers can drive electronic transitions between energy or angular momentum levels in atoms to investigate their internal structure and to run atomic clock and quantum logic experiments. Pictured above is the level structure of a Strontium 87 ion whose different orbitals experience further splittings for slight changes in the transition frequency which are called "Zeeman Sublevels." Often, exciting transitions between particular Zeeman sublevels is advantageous for certain experiments due to the long lifetimes of the excited state and narrow laser frequencies required to drive the transtion.

## The Zeeman Effect

Unfortunately, ambient magnetic fields in the laboratory can shift the Zeeman Sublevels of an atom during the course of an experiment causing a loss in precision and failure of an experiment. Therefore, to run many atomic and molecular optics, or AMO, experiments it is vital to stabilize the magnetic field experienced by the confined atoms or molecules against ambient magnetic field noise. The goal of our project was to generate and stabilize a 3 Guass magnetic field against slow and fast magnetic field drift as well as the 60Hz harmonics from the mains electricity.


# Components

1. MOKU:Go - Microcontroller to act as Oscilloscope, PID loop, and AWG
2. MOSFET N Channel - Transistor with input pin, and sends current from drain to source pins
3. OPAMP LM358AP - Low Noise OP AMP 
4. Bartington Magnetometer - reads magnetic field 0-10G, 3kHz bandwidth 
5. Oscilloscope DS1064 - with option to AC line trigger


# Schematic




## Experimental Setup

Our Experimental Setup consists of two coils which produce the Helmholtz Field at the center (in our case, 3G). The magnetometer is placed at the center of the coils, and the reading is sent to the MOKU:Go. The microcontroller is connected to a laptop, with which we use the MOKU software to create the PID loop and control its parameters. The output is send to a circuit (we implemented it on a breadboard, but optimally a PCB), where we shunt current away current to alter the magnetic field. An oscilloscope is used to line trigger on the AC power wall to implement Feedforward.


## Moku Go
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/3bf59b4830adf94e066e491f6b5c1523c0db8228/Figures/Moku_Go.png" width="1000">
</div>




## N Channel Mosfet
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/ad475d0d4a1821c7e7b7b4b00d3e2eecd4d2d88b/Figures/MOSFET_shunt.png" width="1000">
</div>


## Helmholtz Coils
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/4d71a22e017c13e0bc0db5ba8c13be6a7f2043e5/Figures/helmholtz_coils.png" width="1000">
</div>

## Magnetometer
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/36878cb2ec26542b7947e824e373250a5f17f6a9/Figures/bartington-mag03.png" width="1000">
</div>

# Feedback Control

Our feedback loop consists of a magnetometer, a PID loop in MOKU:Go, and a MOSFET in parallel to the coils shunting current to ground to modulate the field. 

The Bartington Magnetometer is placed at the center of the coils, and sends its reading to the first input pin of the MOKU:Go. The voltage to field ratio of the magnetometer is 1V/G. This is sent to the MOKU's PID loop, where we varied the P and I parameters to reduce the standard deviation as much as possible. The D term was not used as this ended up saturating the PID loop once the external magnetic field became too high. We tuned the parameters to optimize for long term drift cancellation, so Feedforward could handle the faster moving deviations. 

The output of the PID loop was a signal that we sent into a Non-Inverting Amplifier, then to the MOSFET in parallel with our coils. 

The NonInverting Amplifier circuit consisted of an OpAmp, two resistors, and a capacitor. The circuit is below, and the gain of this circuit is 6. The purpose of this circuit is to set the input of the MOSFET in the middle of its range of 0-60 volts. We would then have more control on how much it attenuates the signal. 

<image src="https://github.com/lsever-walter/AMFS/assets/125600843/16d5f4ce-35c8-47ca-8451-a88659c782ef">
  
The output of this circuit was sent to the MOSFET to shunt current accordingly to ground.

## Tuning Controller
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/aeaafa04ac33c4959e7f986978e2067f9bd21d4b/Figures/fb_psd.png" width="1000">
</div>
When the PID feedback was off, there were significant noises in our magnetic field signal that were mostly composed of 60 Hz harmonics. As the feedback was enabled, the standard deviation decreased from 3.9 mG to 0.8 mG. We observed a distinct attenuation of power in small frequencies range of our FFT plot. However, there still remained 60 Hz harmonics peaks that are slightly reduced by PID feedback. By integrating the power spectral density over frequencies from 0 to 300 Hz, above which the PID feedback ceases to effect, we obtained an area ratio of 163.

# Feedforward Control

Feedforward control consists of modifying the input to the system by modulating the source of the disturbance. In this case, the disturbance is the 60Hz from the powerwall that leaks through the DC power supply, as well as 60Hz that enters the magnetic field from laptops and other devices that run at 60Hz. 

Our feedforward methology relies on finding the phase of the 60Hz sin wave in the magnetometer and shunting current to decrease the amplitude of this singal.

## Line Triggering

We AC line triggered from DS1064 Oscilloscope, and produced a TTL (time-to-live) at this frequency and sent this to the Moku:Go. The Moku's AWG produced a sin wave at this frequency. We set the period of this sin wave to be slightly more than 60Hz (~60.05 Hz), so that any error in the TTL's phase did not affect the AWG's produced sin wave.

We then obtained the signal from the magnetometer, and sent this into the MOKU:Go in multi instrument mode. We then phase shifted the sin wave produced by the Moku to be in phase with the 60Hz wave in the magnetometer reading. We then sent the in phase sin wave from the AWG to the second MOSFET in our circuit to shunt away current at this frequency to attenuate 60Hz in the magnetic field.

As a result, the 60Hz in the magnetic field was attenuated. 

## 60Hz Harmonic Cancellation
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/aeaafa04ac33c4959e7f986978e2067f9bd21d4b/Figures/ff_psd%2Binset.png" width="1000">
</div>
The power spectral densities over frequency corresponding to cases of feedforward on and feedforward off are nearly identical, as what we have expected. This is because we were outputing a 60 Hz sinusoidal wave that is in phase with the magnetometer signals, the rest of the spectrum should, therefore, be highly similar. As we zoomed into the region of interest (f = 60 Hz), we observed an approximaely 8 dB attenuation at 60 Hz by subtracting the peaks to their respective noise floors, which are about the same in this case. 

# Feedback and Feedforward
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/aeaafa04ac33c4959e7f986978e2067f9bd21d4b/Figures/ff%2Bfb_psd%2Binset.png" width="1000">
</div>
After the individual implmentation of PID feedback and mains electricity feedforward, we combined both methods to further attenuate the noises in our signal. The standard deviation was reduced to 0.4 mG, as contrast to 0.8 mG for PID feedback alone. There was about 35 dB attenuation of power spectral density at 60 Hz, from which we obtained by subtracting the peak value at 60 Hz from their respective noise floors. Through integrating the power spectral density to the bandwidths of PID feedback alone (f = 300 Hz) and of Feedback and Feedforward (f = 850 Hz), we calculated area ratios of 705 and 65, respectively.

# Future Work
For our future work we hope to implement the stabilization setup developed above on a linear paul trap. We hope to first move optimize our circuits with voltage regulators to protect the operation amplifiers and coils from DC current spikes that could damage the circuitry and potentially the magnetometer. We would then like to implement feedforward for further 60Hz harmonics to attenuate up to 240Hz which would likely increase our PID bandwidth as well. Finally, we would then aim to implement our setup on a linear paul trap by designing new coils to it the ion trap geometry and then use the ion itself to quantify the magnetic field stability in addition to, or perhaps instead of, the magnetometer. 








