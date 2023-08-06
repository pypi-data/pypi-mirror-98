import math
from galpy.potential import MWPotential2014
from galpy.potential import PowerSphericalPotentialwCutoff
from galpy.potential import MiyamotoNagaiPotential
from galpy.potential import NFWPotential
from galpy.util import bovy_conversion
from astropy import units
from galpy.potential import evaluateRforces
from . import read_parameters as par




def MWRfo(ldeg, bdeg, dkpc):


    b = bdeg*par.degtorad
    l = ldeg*par.degtorad
    Rskpc = par.Rskpc
    Vs = par.Vs
    conversion = par.conversion
    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)
    zkpc = dkpc*math.sin(b)
    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)

    #rforce1 = evaluateRforces(MWPotential2014, Rpkpc/Rskpc,zkpc/Rskpc)*bovy_conversion.force_in_kmsMyr(Vs,Rskpc)

    #rfsun = evaluateRforces(MWPotential2014, Rskpc/Rskpc,0.0/Rskpc)*bovy_conversion.force_in_kmsMyr(Vs,Rskpc)

    rforce1 = evaluateRforces(MWPotential2014, Rpkpc/Rskpc,zkpc/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss

    rfsun = evaluateRforces(MWPotential2014, Rskpc/Rskpc,0.0/Rskpc)*((Vs*1000.)**2.)/(Rskpc*par.kpctom) #m/ss
    
    rf0 = rforce1*coslam + rfsun*math.cos(l) #m/ss
    rf = rf0*math.cos(b)/par.c # s-1   
    return rf;




