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
nii = pyfits.open(datadir + "final658.fits")[0].data
sii = pyfits.open(datadir + "final673.fits")[0].data
oi = pyfits.open(datadir + "final631.fits")[0].data

oisii = numpy.log10(oi/sii)
niiha = numpy.log10(nii/ha/2.5)
del(oi); del(sii); del(nii)

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

osvar = bivar.PlotVariable(oisii)
nhvar = bivar.PlotVariable(niiha)
osvar.setminmaxn(min=-0.9, max=0.1)
nhvar.setminmaxn(min=-1.1, max=-0.1)
osvar.settitle(r"\(\log_{10} \mathrm{[O\,I]\,6300}/\mathrm{[S\,II]\,6731}\)", "oi/sii")
nhvar.settitle(r"\(\log_{10} \mathrm{[N\,II]\,6584 / H\alpha}\)", "nii/ha")

g = bivar.Graph(nhvar, osvar, weights=weights, gamma=2.0, statslevel=1)

g.writePDFfile("mos-bivar-oi-sii-nii-ha.pdf")

