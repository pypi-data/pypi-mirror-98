import math
from . import excGal
from . import Shk




def fdotdotSB4cal(ldeg, bdeg, dkpc, mul, mub, f,fdotobs):


    fex_pl = excGal.Expl(ldeg, bdeg, dkpc)

    fex_z = excGal.Exz(ldeg, bdeg, dkpc)

    fex_shk = Shk.Exshk(dkpc, mul, mub)
    
    fex_tot = fex_pl + fex_z + fex_shk


    fex_tot = fex_pl + fex_z + fex_shk
    fourthterm = 2.*fex_tot*(fdotobs/f)
    return fourthterm;

    


