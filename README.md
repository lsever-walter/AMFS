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




# Schematic


## Experimental Setup



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

## PID Controller (Moku Go)


## Tuning Controller
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/aeaafa04ac33c4959e7f986978e2067f9bd21d4b/Figures/fb_psd.png" width="1000">
</div>




# Feedforward Control


## Line Triggering
Discuss 

## 60Hz Harmonic Cancellation
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/aeaafa04ac33c4959e7f986978e2067f9bd21d4b/Figures/ff_psd%2Binset.png" width="1000">
</div>

# Feedback and Feedforward
<div align="center">
<img src="https://github.com/lsever-walter/AMFS/blob/aeaafa04ac33c4959e7f986978e2067f9bd21d4b/Figures/ff%2Bfb_psd%2Binset.png" width="1000">
</div>


# Future Work
For our future work we hope to implement the stabilization setup developed above on a linear paul trap. We hope to first move optimize our circuits with voltage regulators to protect the operation amplifiers and coils from DC current spikes that could damage the circuitry and potentially the magnetometer. We would then like to implement feedforward for further 60Hz harmonics to attenuate up to 240Hz which would likely increase our PID bandwidth as well. Finally, we would then aim to implement our setup on a linear paul trap by designing new coils to it the ion trap geometry and then use the ion itself to quantify the magnetic field stability in addition to, or perhaps instead of, the magnetometer. 








