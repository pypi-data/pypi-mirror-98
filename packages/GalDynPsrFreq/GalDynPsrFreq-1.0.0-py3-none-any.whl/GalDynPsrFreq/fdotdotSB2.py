import math
import numpy as np
from . import read_parameters as par
from galpy.potential import MWPotential2014
from galpy.potential import KeplerPotential
from galpy.potential import evaluatezforces, evaluateRforces, evaluatePotentials
from galpy.potential import evaluatez2derivs,evaluateR2derivs,evaluateRzderivs
from galpy.util import bovy_conversion
from astropy import units as u
from . import excGal
from . import Shk



def fdotdotSB2cal(ldeg,bdeg,dkpc,mul,mub):


   
    Rskpc = par.Rskpc
    Vs = par.Vs
    conversion = par.conversion
    yrts = par.yrts
    c= par.c
    kpctom = par.kpctom
    Rs = Rskpc*kpctom
    mastorad = par.mastorad

    normpottoSI = par.normpottoSI
    normForcetoSI = par.normForcetoSI
    normjerktoSI = par.normjerktoSI


    b = bdeg*par.degtorad
    l = ldeg*par.degtorad

    Rpkpc = par.Rpkpc(ldeg, bdeg, dkpc)

    zkpc = par.z(ldeg, bdeg, dkpc)

    fex_pl = excGal.Expl(ldeg, bdeg, dkpc)

    fex_z = excGal.Exz(ldeg, bdeg, dkpc)

    fex_shk = Shk.Exshk(dkpc, mul, mub)
    
    fex_tot = fex_pl + fex_z + fex_shk


    #mub = mu_alpha #mas/yr
    #mul = mu_delta

    muT = (mub**2. + mul**2.)**0.5  
    #MWPotential2014= [MWPotential2014,KeplerPotential(amp=4*10**6./bovy_conversion.mass_in_msol(par.Vs,par.Rskpc))] 
    MWPot = MWPotential2014  

    appl = evaluateRforces(MWPot, Rpkpc/Rskpc,zkpc/Rskpc)*normForcetoSI
    aspl = evaluateRforces(MWPot, Rskpc/Rskpc,0.0/Rskpc)*normForcetoSI
    apz = evaluatezforces(MWPot, Rpkpc/Rskpc,zkpc/Rskpc)*normForcetoSI



    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)



    res1 = 2.*(mastorad/yrts)*(mub*((math.sin(b)/c)*(appl*coslam + aspl*math.cos(l)) - (math.cos(b)/c)*apz) - mul*(math.sin(l)/c)*(appl*(Rskpc/Rpkpc)-aspl))

    res2 = 2.*fex_tot*(math.cos(b)*math.cos(l)*(aspl/c) + (mastorad/yrts)*mub*(1000.*Vs/c)*math.sin(b)*math.sin(l) - (mastorad/yrts)*mul*(1000.*Vs/c)*math.cos(l))

    res= res1+res2
    return res;


