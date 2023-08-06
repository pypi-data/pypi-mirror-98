import math
import numpy as np
from .fdotdotSB1 import fdotdotSB1cal
from .fdotdotSB2 import fdotdotSB2cal
from .fdotdotSB3 import fdotdotSB3cal
from .fdotdotSB4 import fdotdotSB4cal


def fdotdotexccal(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad):
    
  
    Combterm = fdotdotSB1cal(ldeg,bdeg,dkpc,mul,mub,vrad) + fdotdotSB2cal(ldeg,bdeg,dkpc,mul,mub) + fdotdotSB3cal(ldeg,bdeg,dkpc,mul,mub,vrad) 


    fddotfex = -Combterm + fdotdotSB4cal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs)


    return fddotfex;



