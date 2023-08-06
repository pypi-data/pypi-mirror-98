import math
from galpy.potential import MWPotential2014
from galpy.potential import PowerSphericalPotentialwCutoff
from galpy.potential import MiyamotoNagaiPotential
from galpy.potential import NFWPotential
from galpy.util import bovy_conversion
from astropy import units
from galpy.potential import KeplerPotential
from galpy.potential import evaluateRforces
from . import read_parameters as par



def MWBHRfo(ldeg, bdeg, dkpc):

    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    conversion = par.conversion
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)


    MWPotential2014BH= [MWPotential2014,KeplerPotential(amp=4*10**6./bovy_conversion.mass_in_msol(par.Vs,par.Rskpc))]


    rforce1 = evaluateRforces(MWPotential2014BH, Rpkpc/Rskpc,zkpc/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss

    rfsun = evaluateRforces(MWPotential2014BH, Rskpc/Rskpc,0.0/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss
    
    rf0 = rforce1*coslam + rfsun*math.cos(l) #m/ss
    rf = rf0*math.cos(b)/par.c # s-1
    return rf;


