"""
Plot images of the joint PDF distributions of line ratios from the 
HST Orion mosaics
"""

import numpy
import pyfits
import sys
import bivar
bivar.printextra = 0
bivar.PlotVariable.n = 200                               

import pyx
pyx.text.set(mode="latex")

# Classic diagnostic diagram using nii/ha and oiii/ha (we have no Hbeta)
niiha = numpy.log10(pyfits.open("mos-niiha.fits")[0].data)
oiiiha = -numpy.log10(pyfits.open("mos-haoiii.fits")[0].data)


# Use Ha brightness to make weighting arrays
ha = pyfits.open("mosaicf656-fix.fits")[0].data
ha1 = 150.0
ha2 = 1500.0

# wfaint = numpy.ones(ha.shape)
# wfaint[ha > ha1] = 0
# wbright = numpy.ones(ha.shape)
# wbright[ha < ha2] = 0

wfaint = numpy.exp(-(ha/ha1)**2)
wbright = numpy.exp(-((ha - 2*ha2)/ha2)**2)
wbright[ha > 2*ha2] = 1.0
wbright[ha < ha1] = 0.0
wmid = 1.0 - (wfaint + wbright)
weights = [wfaint, wmid, wbright]
print 'Mean weights: ', wfaint.mean(), wmid.mean(), wbright.mean()
wsum = wfaint + wmid + wbright
print 'Limits of sum of the 3 weights: ', wsum.max(), wsum.min()
del(ha)
del(wsum)

nhvar = bivar.PlotVariable(niiha)
ohvar = bivar.PlotVariable(oiiiha)
nhvar.setminmaxn(min=-1.1, max=-0.1)
ohvar.setminmaxn(min=-1.3, max=-0.3)
nhvar.settitle(r"\(\log_{10} \mathrm{[N\,II]\,6584}/\mathrm{H}\alpha\)", "nii/ha")
ohvar.settitle(r"\(\log_{10} \mathrm{[O\,III]\,5007}/\mathrm{H}\alpha\)", "oiii/ha")

g = bivar.Graph(nhvar, ohvar, weights=weights, gamma=2.0, statslevel=1)

g.writePDFfile("mos-bivar.pdf")

