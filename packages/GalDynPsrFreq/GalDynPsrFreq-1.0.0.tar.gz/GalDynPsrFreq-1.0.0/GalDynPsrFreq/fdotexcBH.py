
import math
from . import excGalBH
from . import Shk
#import GalDynPsrFreq.modelnoBH




def fdotexctotBH(ldeg, bdeg, dkpc, mul, mub):

   fex_pl = excGalBH.Expl(ldeg, bdeg, dkpc)

   fex_z = excGalBH.Exz(ldeg, bdeg, dkpc)

   fex_shk = Shk.Exshk(dkpc, mul, mub)

   fex_tot = fex_pl + fex_z + fex_shk
   return fex_tot;

