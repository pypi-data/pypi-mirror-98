
import math
from .galpyMWBHZfo import MWBHZfo
from .galpyMWBHRfo import MWBHRfo



def Expl(ldeg, bdeg, dkpc):
   excpl = MWBHRfo(ldeg, bdeg, dkpc) #s^-1 
   return -excpl;

def Exz(ldeg, bdeg, dkpc):
   exz = MWBHZfo(ldeg, bdeg, dkpc) #s^-1 
   return -exz;


