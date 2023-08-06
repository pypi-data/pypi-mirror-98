import math
from . import excGal
from . import excGalBH
from . import fdotexc
from . import fdotexcBH
from . import Shk




def fdotExplcal(ldeg, bdeg, dkpc, f):
   Ex_pl = excGal.Expl(ldeg, bdeg, dkpc)
   return Ex_pl*f;


def fdotExzcal(ldeg, bdeg, dkpc, f):
   Ex_z = excGal.Exz(ldeg, bdeg, dkpc)
   return Ex_z*f;


def fdotGalcal(ldeg, bdeg, dkpc, f):
   Ex_pl = excGal.Expl(ldeg, bdeg, dkpc)
   Ex_z = excGal.Exz(ldeg, bdeg, dkpc)
   a = (Ex_pl + Ex_z)*f
   return a;


def fdotExplcalBH(ldeg, bdeg, dkpc, f):
   Ex_pl = excGalBH.Expl(ldeg, bdeg, dkpc)
   return Ex_pl*f;


def fdotExzcalBH(ldeg, bdeg, dkpc, f):
   Ex_z = excGalBH.Exz(ldeg, bdeg, dkpc)
   return Ex_z*f;


def fdotGalcalBH(ldeg, bdeg, dkpc, f):
   Ex_pl = excGalBH.Expl(ldeg, bdeg, dkpc)
   Ex_z = excGalBH.Exz(ldeg, bdeg, dkpc)
   a = (Ex_pl + Ex_z)*f
   return a;



def fdotShk(dkpc, mul, mub, f):
   Ex_shk = Shk.Exshk(dkpc, mul, mub)
   return Ex_shk*f;


def fdotintcal(ldeg, bdeg, dkpc, mul, mub, f, fdotobs):
   a1 = fdotexc.fdotexctot(ldeg, bdeg, dkpc, mul, mub)*f
   a2 = fdotobs - a1
   return a2;

def fdotintcalBH(ldeg, bdeg, dkpc, mul, mub, f, fdotobs):
   a1 = fdotexcBH.fdotexctotBH(ldeg, bdeg, dkpc, mul, mub)*f
   a2 = fdotobs - a1
   return a2;






