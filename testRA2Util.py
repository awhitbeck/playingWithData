from ROOT import *
from RA2Utils import *
from inputFiles import *

RA2 = RA2Util( samples[5].tree )
RA2.getBranches(59)
RA2.dump()
