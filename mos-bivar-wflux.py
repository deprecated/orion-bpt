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


# Weight by surface brghtnesses
ha = pyfits.open("mosaicf656-fix.fits")[0].data
nii = pyfits.open("mosaicf658-fix.fits")[0].data
oiii = pyfits.open("mosaicf502-fix.fits")[0].data
weights = [nii, ha, oiii]

nhvar = bivar.PlotVariable(niiha)
ohvar = bivar.PlotVariable(oiiiha)
nhvar.setminmaxn(min=-1.1, max=-0.1)
ohvar.setminmaxn(min=-1.3, max=-0.3)
nhvar.settitle(r"\(\log_{10} \mathrm{[N\,II]\,6584}/\mathrm{H}\alpha\)", "nii/ha")
ohvar.settitle(r"\(\log_{10} \mathrm{[O\,III]\,5007}/\mathrm{H}\alpha\)", "oiii/ha")

g = bivar.Graph(nhvar, ohvar, weights=weights, gamma=2.0, statslevel=1)

g.writePDFfile("mos-bivar-wflux.pdf")

