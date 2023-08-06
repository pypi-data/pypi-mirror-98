# GalDynPsrFreq Package

GalDynPsrFreq is a package for calculating dynamical contributions to the first and the second derivatives of the frequencies, both spin or orbital, of pulsars in the Galactic field. These dynamical terms depend on the proper motion, the acceleration and the jerk of the pulsars. The main source of the acceleration of the pulsar is the gravitational potential of the Galaxy. GalDynPsrFreq uses a galpy based model of this potential and has the option to include or exclude the effect of the central black hole. 

Details on various dynamical effects and formalism to estimate those are available in Pathak and Bagchi (New Astronomy 85 (2021) 101549; arXiv: 1909.13113). Please cite this paper if you use GalDynPsrFreq for your research.

This package can calculate the fractional contributions or the excess terms, e.g. \dot{f}/f|_excess and \ddot{f}/f|_excess (Eqs. (4) and (11) of Pathak and Bagchi (2021)), where f is either the orbital frequency or the spin frequency. It can also calculate different dynamical terms separately. 

Using the measured values of the frequency, the derivative of the frequency, and the second derivative of the frequency, GalDynPsrFreq can even compute the "intrinsic" values of the frequency derivative, as well as, the frequency second derivative, provided no other extra contribution exists.

A brief outline of the usage of GalDynPsrFreq is given below.

# 1) Install GalDynPsrFreq as pip3 install GalDynPsrFreq (assuming you have numpy, scipy, and galpy already installed and working)

If wished, one can change the values of Rs (Galactocentric cylindrical radius of the Sun) and Vs (rotational speed of the Sun around the Galactic centre) in the parameters.in file that can be found inside the GalDynPsrFreq (installed directory).
But remember that galpy also has these values defined in the file '$home/.galpyrc'. One can in principle change the values in both of the files. However, the Milky Way potential in galpy was fitted with Rs = 8 kpc and Vs = 220 km/s in galpy.


# 2) Import GalDynPsrFreq

import GalDynPsrFreq


# 3)

A) Observable parameters needed to compute \dot{f}/f|_excess and \dot{f}/f|_intrinsic: the Galactic longitude in degrees (say ldeg), the Galactic latitude in degrees (say bdeg), the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), the proper motion in the Galactic latitude in mas/yr (say mub), the frequency in Hz (say f), and the observed frequency derivative in s^{-2} (say fdotobs).

B) Observable parameters needed to compute \ddot{f}/f|_excess and \ddot{f}/f|_intrinsic: the Galactic longitude in degrees (say ldeg), the Galactic latitude in degrees (say bdeg), the distance of the pulsar from the solar system barycenter in kpc (say dkpc), the proper motion in the Galactic longitude in mas/yr (say mul), the proper motion in the Galactic latitude in mas/yr (say mub), the radial component of the relative velocity of the pulsar with respect to the solar system barycenter in km/s (say vrad), the frequency in Hz (say f), the observed frequency derivative in s^{-2} (say fdotobs), and the observed frequency second derivative in s^{-3} (say fdotdotobs). 

The frequency and its derivatives can either be spin or orbital.

# 4) Remember that the model names are case sensitive, so use them as demonstrated below. Also, for each case, ordering of the parameters must be as shown.

# 5) Calculate the Galactic contribution to the excess terms for the first derivative of the frequency using either the model that does not take into account the central black hole contribution to the Milky Way Potential (Model excGal), or the model that takes into account the central black hole (BH) contribution to the Milky Way Potential (Model excGalBH) 
The usage of these models is shown below.

a) When not incorporating the BH contribution to the Milky Way Potential: Model excGal-
GalDynPsrFreq.excGal.Expl(ldeg, bdeg, dkpc) and GalDynPsrFreq.excGal.Exz(ldeg, bdeg, dkpc)

b) When incorporating the BH contribution to the Milky Way Potential: Model excGalBH-
GalDynPsrFreq.excGalBH.Expl(ldeg, bdeg, dkpc) and GalDynPsrFreq.excGalBH.Exz(ldeg, bdeg, dkpc)

The function Expl() calculates the excess term due to the component of the relative acceleration of the pulsar parallel to the Galactic plane and the function Exz() calculates the excess term due to the component of the relative acceleration of the pulsar perpendicular to the Galactic plane. Total dynamical contribution from Galactic potential will be the sum of above two terms. One needs to assign the values of ldeg, bdeg, and dkpc before calling the above functions.


# 6) Calculate the Shklovskii term contribution to the frequency derivative

The Shklovskii term can be calculated as GalDynPsrFreq.Shk.Exshk(dkpc, mul, mub), 

where mul is the proper motion in the Galactic longitude direction (mas/yr) and mub is the proper motion in the Galactic latitude direction (mas/yr). dkpc is as usual the distance of the pulsar from the solar system barycenter in kpc. One needs to assign the values of these parameters first. This term is independent of the Galactic potential model.



# 7) Calculate the total excess terms in the first derivative of the frequency

For total dynamical contributions in the first derivative of the frequency, we use the following modules from GalDynPsrFreq.

a) When not incorporating the BH contribution to the Milky Way Potential: Model fdotexc-
GalDynPsrFreq.fdotexc.fdotexctot(ldeg, bdeg, dkpc, mul, mub)
This uses the modules- excGal.py for the relative acceleration contribution and Shk.py for the Shklovskii effect contribution to the excess terms. 

b) When incorporating the BH contribution to the Milky Way Potential: Model fdotexcBH-
GalDynPsrFreq.fdotexcBH.fdotexctotBH(ldeg, bdeg, dkpc, mul, mub)
This uses the modules- excGalBH.py for the relative acceleration contribution and Shk.py for the Shklovskii effect contribution to the excess terms.

One needs to assign the values of ldeg, bdeg, dkpc, mul, and mub before calling the above functions.



# 8)Print the basic parameters of the pulsars


GalDynPsrFreq.read_parameters.Rskpc returns the Galactocentric cylindrical radius of the Sun (Rs in kpc or Rskpc).

GalDynPsrFreq.read_parameters.Vs returns the rotational speed of the Sun around the Galactic centre (Vs in km/s).

GalDynPsrFreq.read_parameters.Rpkpc(ldeg, bdeg, dkpc) returns the value of Galactocentric cylindrical radius of the pulsar in kpc (Rp in kpc or Rpkpc).

GalDynPsrFreq.read_parameters.z(ldeg, bdeg, dkpc) returns the perpendicular distance of the pulsar from the Galactic plane (z in kpc or zkpc). 

The meaning of the arguments in the above examples are as usual.


# 9) Calculate the intrinsic frequency derivative 
For the frequency derivative calculations we have the fdotint.py module. 

a) When not incorporating the BH contribution to the Milky Way Potential: Model fdotintcal-

The total dynamically caused value of the frequency derivative is the addition of the contribution from the parallel component of the relative acceleration of the pulsar, the perpendicular component of the relative acceleration of the pulsar, and the Shklovskii effect. The intrinsic value of the frequency derivative can be calculated by subtracting that sum from the measured value of the frequency derivative. GalDynPsrFreq can perform this task for us by:

GalDynPsrFreq.fdotint.fdotintcal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs)

Here, in addition to assigning the values of ldeg, bdeg, dkpc, mul, and mub, one needs to also assign the values of the frequency 'f' in Hz, and the measured value of the frequency derivative 'fdotobs' in seconds^(-2).

Additionally, the individual contributions can also be calculated using the fdotint.py module in GalDynPsrFreq as,

GalDynPsrFreq.fdotint.fdotExplcal(ldeg, bdeg, dkpc, f) # due to the parallel component of the relative acceleration of the pulsar
GalDynPsrFreq.fdotint.fdotExzcal(ldeg, bdeg, dkpc, f) # due to the perpendicular component of the relative acceleration of the pulsar
GalDynPsrFreq.fdotint.fdotGalcal(ldeg, bdeg, dkpc, f) # due to the sum of the parallel and the perpendicular components of the relative acceleration of the pulsar

For the above 3 terms, in addition to assigning the values of ldeg, bdeg, dkpc, mul, and mub, one needs to also assign the values of the frequency, 'f', in Hz.
 

b) When incorporating the BH contribution to the Milky Way Potential: Model fdotintcalBH-

As explained in a) part, The intrinsic value of the frequency derivative can be calculated by:

GalDynPsrFreq.fdotint.fdotintcalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs)

Here, in addition to assigning the values of ldeg, bdeg, dkpc, mul, and mub, one needs to also assign the values of the frequency 'f' in Hz, and the measured value of the frequency derivative 'fdotobs' in seconds^(-2).


Additionally, the individual contributions can also be calculated using the fdotint.py module in GalDynPsrFreq as,

GalDynPsrFreq.fdotint.fdotExplcalBH(ldeg, bdeg, dkpc, f) # due to the parallel component of the relative acceleration of the pulsar
GalDynPsrFreq.fdotint.fdotExzcalBH(ldeg, bdeg, dkpc, f) # due to the perpendicular component of the relative acceleration of the pulsar
GalDynPsrFreq.fdotint.fdotGalcalBH(ldeg, bdeg, dkpc, f) # due to the sum of the parallel and the perpendicular components of the relative acceleration of the pulsar

For the above 3 terms, in addition to assigning the values of ldeg, bdeg, dkpc, mul, and mub, one needs to also assign the values of the frequency 'f' in Hz.


c) For calculating the contribution of the Shklovskii effect, separately, to the frequency derivative, we can use,
 
GalDynPsrFreq.fdotint.fdotShk(dkpc, mul, mub, f)

Here, in addition to assigning the values of dkpc, mul, and mub, one needs to also assign the value of the frequency, 'f', in Hz.




# 10) Calculate the excess terms in the second derivative of the frequency 

For dynamical contributions in the second derivative of the frequency, we use the following modules from GalDynPsrFreq.

a)When not incorporating the BH contribution to the Milky Way Potential: Model fdotdotexc-
GalDynPsrFreq.fdotdotexc.fdotdotexccal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad) 

This module internally calls the modules for calculating the first, the second, the third, and the fourth sqaure bracket terms (which don't incorporate the BH contribution). These modules can also be directly called as-
GalDynPsrFreq.fdotdotSB1.fdotdotSB1cal(ldeg, bdeg, dkpc, mul, mub, vrad) #for calculating the first square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
GalDynPsrFreq.fdotdotSB2.fdotdotSB2cal(ldeg, bdeg, dkpc, mul, mub) #for calculating the second square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
GalDynPsrFreq.fdotdotSB3.fdotdotSB3cal(ldeg, bdeg, dkpc, mul, mub, vrad) #for calculating the third square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
GalDynPsrFreq.fdotdotSB4.fdotdotSB4cal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs) #for calculating the fourth square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)

b) When incorporating the BH contribution to the Milky Way Potential: Model fdotdotexcBH-
GalDynPsrFreq.fdotdotexcBH.fdotdotexccalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad)

This module internally calls the modules for calculating the first, the second, the third, and the fourth sqaure bracket terms (which incorporate the BH contribution). These modules can also be directly called as-
GalDynPsrFreq.fdotdotSB1BH.fdotdotSB1calBH(ldeg, bdeg, dkpc, mul, mub, vrad) #for calculating the first square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
GalDynPsrFreq.fdotdotSB2BH.fdotdotSB2calBH(ldeg, bdeg, dkpc, mul, mub) #for calculating the second square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
GalDynPsrFreq.fdotdotSB3BH.fdotdotSB3calBH(ldeg, bdeg, dkpc, mul, mub, vrad) #for calculating the third square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
GalDynPsrFreq.fdotdotSB4BH.fdotdotSB4calBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs) #for calculating the fourth square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021)
  

Here, for both the cases, in addition to assigning the values of ldeg, bdeg, dkpc, mul, mub, f, and fdotobs, one needs to also assign the measured value of the radial component of the relative velocity of the pulsar, 'vrad', in km/s.


# 11) Calculate the intrinsic second derivative of the frequency 

For calculating the intrinsic value of the second derivative of the frequency, we use the following modules from GalDynPsrFreq.

a)When not incorporating the BH contribution to the Milky Way Potential: Model fdotdotintcal-
GalDynPsrFreq.fdotdotint.fdotdotintcal(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad,fdotdotobs) 

b) When incorporating the BH contribution to the Milky Way Potential: Model fdotdotintcalBH-
GalDynPsrFreq.fdotdotint.fdotdotintcalBH(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad,fdotdotobs)

Here, for both the cases, in addition to assigning the values of ldeg, bdeg, dkpc, mul, mub, f, fdotobs, and vrad, one needs to also assign the measured value of the second derivative of the frequency, 'fdotdotobs', in seconds^(-3).

## All the above points will be clearer from the following demonstration 


### Call GalDynPsrFreq as:


import GalDynPsrFreq


##  Provide the following values in your code 

### ldeg = Galactic longitude in degrees, bdeg = Galactic latitude in degrees, dkpc = distance to pulsar in kpc


ldeg = 20.0

bdeg = 20.0

dkpc = 2.0

### #####Extract important parameters, say, values of Rp (in kpc) and z (in kpc)#####

Rpkpc = GalDynPsrFreq.read_parameters.Rpkpc(ldeg, bdeg, dkpc)

zkpc = GalDynPsrFreq.read_parameters.z(ldeg, bdeg, dkpc)


### #####Compute the excess Shklovskii term for the first derivative of the frequency using Exshk()#####

### We need to provide the values of the proper motion in the Galactic longitude direction and the proper motion in the Galactic latitude direction

### mul = proper motion in the Galactic longitude direction (in mas/yr), mub = proper motion in the Galactic latitude direction (in mas/yr)

mul = 20.0
mub = 20.0

ExcessSh = GalDynPsrFreq.Shk.Exshk(dkpc, mul, mub)



### #####Compute the excess terms for the first derivative of the frequency due to the Galactic potential#####

### =====Model excGal (not incorporating the BH contribution to the Milky Way Potential)=====

fex_pl = GalDynPsr.excGal.Expl(ldeg, bdeg, dkpc) #calculates the contribution to the excess term due to the parallel component of the relative acceleration of the pulsar

fex_z = GalDynPsr.excGal.Exz(ldeg, bdeg, dkpc) #calculates the contribution to the excess term due to the perpendicular component of the relative acceleration of the pulsar

totalfexGal = fex_pl+fex_z

-------------------------------------OR------------------------------------------

### =====Model excGalBH (incorporating the BH contribution to the Milky Way Potential)=====

fex_pl = GalDynPsrFreq.excGalBH.Expl(ldeg, bdeg, dkpc) #calculates the contribution to the excess term due to the parallel component of the relative acceleration of the pulsar

fex_z = GalDynPsrFreq.excGalBH.Exz(ldeg, bdeg, dkpc) #calculates the contribution to the excess term due to the perpendicular component of the relative acceleration of the pulsar

totalfexGal = fex_pl+fex_z



### #####Compute the total excess term for the first derivative of the frequency#####

### =====Model fdotexc (not incorporating the BH contribution to the Milky Way Potential)=====
fdotfex = GalDynPsrFreq.fdotexc.fdotexctot(ldeg, bdeg, dkpc, mul, mub)

-------------------------------------OR------------------------------------------

### =====Model fdotexcBH (incorporating the BH contribution to the Milky Way Potential)=====
fdotfex = GalDynPsrFreq.fdotexcBH.fdotexctotBH(ldeg, bdeg, dkpc, mul, mub)


### #####Compute the intrinsic value of the first derivative of the frequency#####

### Additional observable parameters required for the spin (or orbital) frequency derivative calcuations: f = frequency in Hz, fdotobs = measured value of the frequency derivative in s^-2
 
f = 50.0

fdotobs = -1.43e-15


### =====Model fdotintcal (not incorporating the BH contribution to the Milky Way Potential)=====

fdot_int = GalDynPsrFreq.fdotint.fdotintcal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs) #calculates the intrinsic frequency derivative

-------------------------------------OR------------------------------------------

### =====Model fdotintcalBH (incorporating the BH contribution to the Milky Way Potential)=====

fdot_int = GalDynPsrFreq.fdotint.fdotintcalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs) #calculates the intrinsic frequency derivative


### #####Additional Terms from module fdotint.py#####

fdot_Shk = GalDynPsrFreq.fdotint.fdotShk(dkpc, mul, mub,f) #calculates the Shklovskii contribution to the frequency derivative

### =====When not incorporating the BH contribution to the Milky Way Potential=====

fdot_Expl = GalDynPsrFreq.fdotint.fdotExplcal(ldeg, bdeg, dkpc, f) #calculates the contribution to the frequency derivative due to the parallel component of the relative acceleration of the pulsar

fdot_Exz = GalDynPsrFreq.fdotint.fdotExzcal(ldeg, bdeg, dkpc, f) #calculates the contribution to the frequency derivative due to the perpendicular component of the relative acceleration of the pulsar
 
fdot_Gal = GalDynPsrFreq.fdotint.fdotGalcal(ldeg, bdeg, dkpc, f) #calculates the sum of parallel and perpendicular contributions to the frequency derivative

-------------------------------------OR------------------------------------------

### =====When incorporating the BH contribution to the Milky Way Potential=====

fdot_Expl = GalDynPsrFreq.fdotint.fdotExplcalBH(ldeg, bdeg, dkpc, f) #calculates the contribution to the frequency derivative due to the parallel component of the relative acceleration of the pulsar 

fdot_Exz = GalDynPsrFreq.fdotint.fdotExzcalBH(ldeg, bdeg, dkpc, f) #calculates the contribution to the frequency derivative due to the perpendicular component of the relative acceleration of the pulsar
 
fdot_Gal = GalDynPsrFreq.fdotint.fdotGalcalBH(ldeg, bdeg, dkpc, f) #calculates the sum of parallel and perpendicular contributions to the frequency derivative



### #####Compute the excess term for second derivative of the frequency#####
### Additional observable parameters required: vrad = radial component of the relative velocity of the pulsar in km/s

vrad = 20.0

### =====Model fdotdotexc (not incorporating the BH contribution to the Milky Way Potential)=====

fddotfex = GalDynPsrFreq.fdotdotexc.fdotdotexccal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad)

-------------------------------------OR------------------------------------------

### =====Model fdotdotexcBH (incorporating the BH contribution to the Milky Way Potential)=====

fddotfex = GalDynPsrFreq.fdotdotexcBH.fdotdotexccalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad)



### #####Compute the intrinsic value of the second derivative of the frequency#####
### Additional observable parameters required: fdotdotobs = observed second derivative of the frequency in s^-3

fdotdotobs = 1.2e-28

### =====Model fdotdotintcal (not incorporating the BH contribution to the Milky Way Potential)=====

fddotint = GalDynPsrFreq.fdotdotint.fdotdotintcal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad, fdotdotobs)

-------------------------------------OR------------------------------------------ 

### =====Model fdotdotintcalBH (incorporating the BH contribution to the Milky Way Potential)=====

fddotint = GalDynPsrFreq.fdotdotint.fdotdotintcalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad, fdotdotobs)





### #####Example#####

### Using models excGalBH and fdotdotexcBH  

import GalDynPsrFreq

ldeg = 20.0

bdeg= 20.0

dkpc = 2.0

mul = 20.0

mub = 20.0

vrad = 20.0

f = 50.0

fdotobs = -1.43e-15

fdotdotobs = 1.2e-28

Rpkpc = GalDynPsrFreq.read_parameters.Rpkpc(ldeg, bdeg, dkpc) <br/>
Output: 6.267007084433072

zkpc = GalDynPsrFreq.read_parameters.z(ldeg, bdeg, dkpc) <br/>
Output: 0.6840402866513374

fex_pl = GalDynPsrFreq.excGalBH.Expl(ldeg, bdeg, dkpc) <br/>
Output: -1.117390734484584e-19

fex_z = GalDynPsrFreq.excGalBH.Exz(ldeg, bdeg, dkpc) <br/>
Output: 1.0790292219978148e-19

fex_shk = GalDynPsrFreq.Shk.Exshk(dkpc, mul, mub) <br/>
Output: -3.886794901984e-18


fdot_Expl =  GalDynPsrFreq.fdotint.fdotExplcalBH(ldeg, bdeg, dkpc, f) <br/>
Output: -5.58695367242292e-18

fdot_Exz =  GalDynPsrFreq.fdotint.fdotExzcalBH(ldeg, bdeg, dkpc, f) <br/>
Output: 5.395146109989074e-18

fdot_Gal =  GalDynPsrFreq.fdotint.fdotGalcalBH(ldeg, bdeg, dkpc, f) <br/>
Output: -1.9180756243384537e-19

fdot_Shk =  GalDynPsrFreq.fdotint.fdotShk(dkpc, mul, mub, f) <br/>
Output: -1.9433974509920001e-16

fdot_int = GalDynPsrFreq.fdotint.fdotintcalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs) <br/>
Output: -1.2354684473383662e-15


fddotfex = GalDynPsrFreq.fdotdotexcBH.fdotdotexccalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad) <br/>
Output: 1.3893598943987592e-34

fddotint = GalDynPsrFreq.fdotdotint.fdotdotintcalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad, fdotdotobs) <br/>
Output: 1.1999305320052803e-28




#========================================================================================
### #####Contents of the Package#####

Files:

parameters.in: Input file, that contains values of constants which are subject to change with improvements in measurements. User can change the values of the constants if the need be. These constants are Vs (rotational speed of the Sun around the Galactic centre in km/s) and Rskpc (Galactocentric radius of the Sun, Rs, in kpc). Rs is defined in a cylindrical coordinate system. 

README.txt: Contents of this README.md file inside package along with code files.

Description of different codes:

read_parameters.py: Contains various constants used in the package, as well as, functions to calculate Rp(kpc) and z(kpc). 

excGal.py: Calculates the parallel, as well as, the perpendicular components of the Galactic contribution to the excess terms for the first frequency derivative without incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

excGalBH.py: Calculates the parallel, as well as, the perpendicular components of the Galactic contribution to the excess terms for the first frequency derivative incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

Shk.py: Calculates the Shklovskii term d(mu_T*mu_T)/c, where d is the distance of the pulsar from the solar system barycentre, mu_T is the total proper motion of the pulsar, and c is the speed of light. The required arguments for this module are the observables dkpc, mul, and mub.

galpyMWRfo.py: Calculates (parallel component of relative acceleration)/c using `evaluateRforces' function in galpy without incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

galpyMWBHRfo.py: Calculates (parallel component of relative acceleration)/c using `evaluateRforces' function in galpy incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

galpyMWZfo.py: Calculates (perpendicular component of relative acceleration)/c using `evaluatezforces' function in galpy without incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

galpyMWBHZfo.py: Calculates (perpendicular component of relative acceleration)/c using `evaluatezforces' function in galpy incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are the observables ldeg, bdeg, and dkpc.

fdotexc.py: Calculates the total excess term in the first derivative of the frequency without incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, and mub.

fdotexcBH.py: Calculates the total excess term in the first derivative of the frequency incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, and mub.

fdotint.py: Calculates the intrinsic frequency derivative for both cases- when the contribution of the central black hole to the gravitational potential of the Milky Way is not included (Model fdotintcal) and when that contribution is included (Model fdotintcalBH). The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, and f. Also, this module can separately calculate the individual frequency derivative contributions from the parallel and the perpendicular components of relative acceleration, and from the Shklovskii term. 

fdotdotSB1.py: Calculates the first square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) without the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, and vrad.

fdotdotSB2.py: Calculates the second square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) without the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, and mub.

fdotdotSB3.py: Calculates the third square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) without the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, and vrad.

fdotdotSB4.py: Calculates the fourth square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) without the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, and fdotobs.

fdotdotSB1BH.py: Calculates the first square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) incorporating the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, and vrad.

fdotdotSB2BH.py: Calculates the second square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) incorporating the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, and mub.

fdotdotSB3BH.py: Calculates the third square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) incorporating the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, and vrad.

fdotdotSB4BH.py: Calculates the fourth square bracket term of Eq. (11) of the paper Pathak and Bagchi (2021) incorporating the contribution of the central black hole. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, and fdotobs.

fdotdotexc.py: Model fdotdotexc- Calculates the total excess term for the second derivative of the frequency without incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, fdotobs, and vrad.

fdotdotexcBH.py: Model fdotdotexcBH- Calculates the total excess term for the second derivative of the frequency incorporating the effect of the central black hole in the gravitational potential of the Milky Way. The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, fdotobs, and vrad.

fdotdotint.py: Calculates the intrinsic value of the second derivative of the frequency for both cases, i.e.,  when the contribution of the central black hole to the gravitational potential of the Milky Way is not included (Model fdotdotintcal) and when that contribution is included (Model fdotdotintcalBH). The required arguments for this module are ldeg, bdeg, dkpc, mul, mub, f, fdotobs, vrad, and fdotdotobs. 

############################################################


