"""
Attempt to transform the line ratios to new axes (A, B)

Axis A is in the sense of increasing ionization
Axis B is at 90 degrees
"""

import numpy
import pyfits


datadir = "/Users/will/Work/RubinWFC3/" 

f502 =  pyfits.open(datadir + "F502N.fits")[0]
f658 =  pyfits.open(datadir + "F658N.fits")[0]
f656 =  pyfits.open(datadir + "F656N.fits")[0]

r658656 = numpy.log10(f658.data/f656.data)
r502656 = numpy.log10(f502.data/f656.data)

A = f502.copy()
B = f502.copy()
A.data = -r658656 + r502656
B.data = r658656 + r502656

A.writeto(datadir + "rubin-NHO-A.fits", clobber=True)
B.writeto(datadir + "rubin-NHO-B.fits", clobber=True)
