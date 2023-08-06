
import math
import numpy as np
from . import read_parameters as par



def Exshk(dkpc, mul, mub):
  c= par.c
  mu_T = pow((mul*mul + mub*mub),0.5) # mas/yr
  fshk = -(dkpc*(mu_T*mu_T))/c #kpc*(mass yr-1)/(m/s)
  fshks = -(2.42924681374e-21)*dkpc*(mu_T*mu_T) #s^-1
  return fshks;


