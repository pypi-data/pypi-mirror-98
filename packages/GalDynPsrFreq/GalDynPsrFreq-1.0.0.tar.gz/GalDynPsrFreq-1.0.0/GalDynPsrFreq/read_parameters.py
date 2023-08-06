import math
import pkg_resources



global pi,degtorad,dtoyr,c,kpctom,yrts,Vs,Rskpc,conversion,Vs,Rskpc,mastorad,normpottoSI,normForcetoSI,normjerktoSI 
pi = math.pi
degtorad= pi/180.0
dtoyr = 1.0/365.25
c = 299792458.0 #m/s
kpctom = 3.0856775814913675e+19
yrts = 365.25*24.0*3600.0
conversion = 1000.0/(c*yrts*pow(10.0,6.0))


mastorad = 4.8481368110953594e-09




DB_FILE = pkg_resources.resource_filename(__name__, 'parameters.in')

inp = open(DB_FILE,'r')
x=[]
for line in inp:
   s=line.split() 
   x.append(s)

Vs = float(x[0][2])

Rskpc = float(x[1][2])
 


normpottoSI = (Vs*1000.)**2.
normForcetoSI = ((Vs*1000.)**2.)/(Rskpc*kpctom)
normjerktoSI = ((Vs*1000.)**2.)/((Rskpc*kpctom)**2.)

def Rpkpc(ldeg, bdeg, dkpc):
     l = ldeg*degtorad
     b = bdeg*degtorad     
     a = Rskpc*Rskpc + dkpc*math.cos(b)*dkpc*math.cos(b) - 2.0*Rskpc*dkpc*math.cos(b)*math.cos(l)
     asqrt = pow(a,0.5)
     return asqrt;


def z(ldeg, bdeg, dkpc):
    b = bdeg*degtorad
    zkpc = dkpc*math.sin(b)
    return zkpc;



inp.close()




