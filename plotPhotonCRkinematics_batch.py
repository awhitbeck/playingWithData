from ROOT import *
from math import *
from inputFiles import *
from commissioningUtils import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

######################################
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--samples", dest="samplesRaw", default="Gjets400",
                  help="list of samples to run over - samples should be separated by a comma" )

(options, args) = parser.parse_args()
sampleList = options.samplesRaw.split(",")
###################################################

lumi = 40.03

histo = {}

samples.extend( dataSamples )

for s in samples : 

    if not s.tag in sampleList : continue 

    outFile = TFile("photonCRkin_{0}.root".format(s.tag),"RECREATE")

    histo[s] = plotPhotonCRHisto(s,-1)
    for key in histo[s] : 
        histo[s][key].SetFillColor(s.color)
        histo[s][key].SetLineColor(s.color)
        histo[s][key].GetXaxis().SetNdivisions(505)
        #histo[s][key].Scale(lumi)
        histo[s][key].Write()

    outFile.Close()
