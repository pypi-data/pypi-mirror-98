import math
from . import fdotdotexc
from . import fdotdotexcBH

def fdotdotintcal(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad,fdotdotobs):
    fddotfex = fdotdotexc.fdotdotexccal(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad)
    fddotint = fdotdotobs-f*fddotfex
    return fddotint;

def fdotdotintcalBH(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad,fdotdotobs):
    fddotfex = fdotdotexcBH.fdotdotexccalBH(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad)
    fddotint = fdotdotobs-f*fddotfex
    return fddotint;
