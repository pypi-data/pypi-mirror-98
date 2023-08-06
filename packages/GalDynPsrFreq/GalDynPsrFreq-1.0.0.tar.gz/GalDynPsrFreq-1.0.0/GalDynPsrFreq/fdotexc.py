
import math
from . import excGal
from . import Shk
#import GalDynPsrFreq.modelnoBH




def fdotexctot(ldeg, bdeg, dkpc, mul, mub):

   fex_pl = excGal.Expl(ldeg, bdeg, dkpc)

   fex_z = excGal.Exz(ldeg, bdeg, dkpc)

   fex_shk = Shk.Exshk(dkpc, mul, mub)

   fex_tot = fex_pl + fex_z + fex_shk
   return fex_tot;



