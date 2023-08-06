
import math
from .galpyMWZfo import MWZfo
from .galpyMWRfo import MWRfo




def Expl(ldeg, bdeg, dkpc):
   excpl = MWRfo(ldeg, bdeg, dkpc) #s^-1 
   return -excpl;

def Exz(ldeg, bdeg, dkpc):
   exz = MWZfo(ldeg, bdeg, dkpc) #s^-1 
   return -exz;


