import math
import numpy as np
from . import read_parameters as par
from . import excGalBH
from . import Shk
from galpy.potential import MWPotential2014
from galpy.potential import KeplerPotential
from galpy.potential import evaluatezforces, evaluateRforces, evaluatePotentials
from galpy.potential import evaluatez2derivs,evaluateR2derivs,evaluateRzderivs
from galpy.util import bovy_conversion
from astropy import units as u

def fdotdotSB3calBH(ldeg,bdeg,dkpc,mul,mub,vrad):

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

    fex_pl = excGalBH.Expl(ldeg, bdeg, dkpc)

    fex_z = excGalBH.Exz(ldeg, bdeg, dkpc)

    fex_shk = Shk.Exshk(dkpc, mul, mub)
    
    fex_tot = fex_pl + fex_z + fex_shk


    #mub = mu_alpha #mas/yr
    #mul = mu_delta

    muT = (mub**2. + mul**2.)**0.5  
    #MWPotential2014= [MWPotential2014,KeplerPotential(amp=4*10**6./bovy_conversion.mass_in_msol(par.Vs,par.Rskpc))] 
    MWPot = [MWPotential2014,KeplerPotential(amp=4*10**6./bovy_conversion.mass_in_msol(par.Vs,par.Rskpc))]  

    appl = evaluateRforces(MWPot, Rpkpc/Rskpc,zkpc/Rskpc)*normForcetoSI
    aspl = evaluateRforces(MWPot, Rskpc/Rskpc,0.0/Rskpc)*normForcetoSI
    apz = evaluatezforces(MWPot, Rpkpc/Rskpc,zkpc/Rskpc)*normForcetoSI



    be = (dkpc/Rskpc)*math.cos(b) - math.cos(l)
    coslam =  be*(Rskpc/Rpkpc)
    coslpluslam = math.cos(l)*coslam - (Rskpc*math.sin(l)/Rpkpc)*math.sin(l)

    aTl1 = -(appl*(Rskpc*math.sin(l)/Rpkpc)-aspl*math.sin(l))
    aTb1 = appl*coslam*math.sin(b)-apz*math.cos(b) + aspl*math.cos(l)*math.sin(b)
    aTnet1 = (aTl1**2. + aTb1**2.)**(0.5)
    alphaV1 = math.atan2(mub,mul)/par.degtorad
    alphaA1 = math.atan2(aTb1,aTl1)/par.degtorad
    if alphaV1 < 0.:
       alphaV = 360.+alphaV1
    else:
       alphaV = alphaV1

    if alphaA1 < 0.:
       alphaA = 360.+alphaA1
    else:
       alphaA = alphaA1
    alpha = abs(alphaA - alphaV)



    aT1 = 2.*appl*aspl*coslpluslam
    aT2 = (c*(fex_pl+fex_z))**2.
    aTsq = appl**2. + aspl**2. + aT1 + apz**2. - aT2
    #if aTsq < 0.0:
    aT =  (appl**2. + aspl**2. + aT1 + apz**2. - aT2)**0.5




    yrts = par.yrts
    c= par.c
    mastorad = par.mastorad

    #tsbvrad = (1./c)*(3.*(1000.0*vrad)*(((mastorad/yrts)*muT)**2.)) 
    tsbt = (1./c)*(aT*((mastorad/yrts)*muT)*math.cos(alpha) - 3.*(1000.0*vrad)*(((mastorad/yrts)*muT)**2.))
    return tsbt;

