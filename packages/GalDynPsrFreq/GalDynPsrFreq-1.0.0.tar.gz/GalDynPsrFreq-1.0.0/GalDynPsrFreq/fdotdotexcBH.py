import math
import numpy as np
from .fdotdotSB1BH import fdotdotSB1calBH
from .fdotdotSB2BH import fdotdotSB2calBH
from .fdotdotSB3BH import fdotdotSB3calBH
from .fdotdotSB4BH import fdotdotSB4calBH


def fdotdotexccalBH(ldeg,bdeg,dkpc,mul,mub,f,fdotobs,vrad):
         
  
    Combterm = fdotdotSB1calBH(ldeg,bdeg,dkpc,mul,mub,vrad) + fdotdotSB2calBH(ldeg,bdeg,dkpc,mul,mub) + fdotdotSB3calBH(ldeg,bdeg,dkpc,mul,mub,vrad) 


    fddotfex = -Combterm + fdotdotSB4calBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs)
   

    return fddotfex;


    
 
