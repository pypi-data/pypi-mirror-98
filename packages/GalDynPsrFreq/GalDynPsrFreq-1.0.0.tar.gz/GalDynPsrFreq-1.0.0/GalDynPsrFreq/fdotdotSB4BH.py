import math
from . import excGalBH
from . import Shk




def fdotdotSB4calBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs):


    fex_pl = excGalBH.Expl(ldeg, bdeg, dkpc)

    fex_z = excGalBH.Exz(ldeg, bdeg, dkpc)

    fex_shk = Shk.Exshk(dkpc, mul, mub)
    
    fex_tot = fex_pl + fex_z + fex_shk


    fex_tot = fex_pl + fex_z + fex_shk
    fourthterm = 2.*fex_tot*(fdotobs/f)
    return fourthterm;

    


