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
oinii = pyfits.open(datadir + "final631-658-sub0.09.fits")[0].data
siinii = pyfits.open(datadir + "final673-658.fits")[0].data

# Use Ha brightness to make weighting arrays
ha = pyfits.open(datadir + "final656.fits")[0].data
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

onvar = bivar.PlotVariable(oinii)
snvar = bivar.PlotVariable(siinii)
onvar.setminmaxn(min=-1.6, max=-0.6)
snvar.setminmaxn(min=-0.9, max=0.1)
onvar.settitle(r"\(\log_{10} \mathrm{[O\,I]\,6300}/\mathrm{[N\,II]\,6584}\)", "oi/nii")
snvar.settitle(r"\(\log_{10} \mathrm{[S\,II]\,6731}/\mathrm{[N\,II]\,6584}\)", "sii/nii")

g = bivar.Graph(onvar, snvar, weights=weights, gamma=2.0, statslevel=1)

g.writePDFfile("mos-bivar-oi-sii.pdf")

