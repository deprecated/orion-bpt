"""
Attempt to transform the line ratios to new axes (A, B)

Axis A is in the sense of increasing ionization
Axis B is at 90 degrees
"""

import numpy
import pyfits

datadir = "../2002/" 
r631658 = pyfits.open(datadir + "final631-658-sub0.09.fits")[0]
r673658 = pyfits.open(datadir + "final673-658.fits")[0]


A = r631658.copy()
B = r673658.copy()
A.data = r631658.data + r673658.data
B.data = r631658.data - r673658.data
A.writeto(datadir + "OSN-A.fits", clobber=True)
B.writeto(datadir + "OSN-B.fits", clobber=True)

f502 =  pyfits.open("mosaicf502-fix.fits")[0]
f658 =  pyfits.open("mosaicf658-fix.fits")[0]
f656 =  pyfits.open("mosaicf656-fix.fits")[0]

r658656 = numpy.log10(f658.data/f656.data)
r502656 = numpy.log10(f502.data/f656.data)

A = f502.copy()
B = f502.copy()
A.data = -r658656 + r502656
B.data = r658656 + r502656

A.writeto("NHO-A.fits", clobber=True)
B.writeto("NHO-B.fits", clobber=True)
