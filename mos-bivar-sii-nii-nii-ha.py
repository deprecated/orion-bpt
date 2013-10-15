"""
Plot images of the joint PDF distributions of line ratios from the 
HST Orion mosaics

This one does sii/nii versus oi/nii
"""

import numpy
import pyfits
import sys
import bivar
bivar.printextra = 0
bivar.PlotVariable.n = 200                               

import pyx
pyx.text.set(mode="latex")

datadir = "../2002/" 

# Classic diagnostic diagram using nii/ha and oiii/ha (we have no Hbeta)
ha = pyfits.open(datadir + "final656.fits")[0].data
siinii = pyfits.open(datadir + "final673-658.fits")[0].data
niiha = pyfits.open(datadir + "final658-656.fits")[0].data

# Use Ha brightness to make weighting arrays
ha1 = 150.0
ha2 = 1500.0
wfaint = numpy.exp(-(ha/ha1)**2)
wbright = numpy.exp(-((ha - 2*ha2)/ha2)**2)
wbright[ha > 2*ha2] = 1.0
wbright[ha < ha1] = 0.0
wmid = 1.0 - (wfaint + wbright)
weights = [wfaint, wmid, wbright]
print 'Mean weights: ', wfaint.mean(), wmid.mean(), wbright.mean()
wsum = wfaint + wmid + wbright
print 'Limits of sum of the 3 weights: ', wsum.max(), wsum.min()

# weights = [w*ha for w in weights]

del(ha)
del(wsum)

yvar = bivar.PlotVariable(siinii)
xvar = bivar.PlotVariable(niiha)
yvar.setminmaxn(min=-0.9, max=0.1)
xvar.setminmaxn(min=-1.1, max=-0.1)
yvar.settitle(r"\(\log_{10} \mathrm{[S\,II]\,6731/ [N\,II]\,6584}\)", "sii/nii")
xvar.settitle(r"\(\log_{10} \mathrm{[N\,II]\,6584 / H\alpha}\)", "nii/ha")

g = bivar.Graph(xvar, yvar, weights=weights, gamma=2.0, statslevel=1)

g.writePDFfile("mos-bivar-sii-nii-nii-ha.pdf")

