import math
from galpy.potential import MWPotential2014
from galpy.potential import PowerSphericalPotentialwCutoff
from galpy.potential import MiyamotoNagaiPotential
from galpy.potential import NFWPotential
from galpy.util import bovy_conversion
from galpy.potential import evaluatezforces
from astropy import units
from galpy.potential import KeplerPotential
from . import read_parameters as par


 

def MWBHZfo(ldeg, bdeg, dkpc):

    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    conversion = par.conversion
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
  
    MWPotential2014BH= [MWPotential2014,KeplerPotential(amp=4*10**6./bovy_conversion.mass_in_msol(par.Vs,par.Rskpc))]
    zf1 = evaluatezforces(MWPotential2014BH, Rpkpc/Rskpc,zkpc/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss
    Excz = zf1*math.sin(b)/par.c #s-1
    return Excz;


