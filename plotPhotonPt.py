from ROOT import *
from labels import *
from math import *
from inputFiles import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

histoTemplate = TH1F("Zmass",";p_{T,#gamma};Events",50,50,350)
lumi = 0.006

def plotHisto( sample , maxEvents ) :
    
    histo_ = TH1F( histoTemplate )
    histo_.SetName(sample.tag)

    numEvents = sample.tree.GetEntries()

    for iEvt in range( numEvents ) : 

        if iEvt > maxEvents and maxEvents != -1 : break

        sample.tree.GetEntry(iEvt)

        if iEvt % 10000 == 0 : 
            print "event:",iEvt

        HT = getattr(sample.tree,"HT")
        photons = getattr(sample.tree,"photonCands")
        hOverE = getattr(sample.tree,"photon_hadTowOverEM")
        sieie = getattr(sample.tree,"photon_sigmaIetaIeta")
        isEB = getattr(sample.tree,"photon_isEB")
        pixelSeed = getattr(sample.tree,"photon_hasPixelSeed")
        eleVeto = getattr(sample.tree,"photon_hasPixelSeed")
        run = getattr(sample.tree,"RunNum")
        photIso = getattr(sample.tree,"photon_pfGammaIsoRhoCorr")
        neutIso = getattr(sample.tree,"photon_pfNeutralIsoRhoCorr")
        charIso = getattr(sample.tree,"photon_pfChargedIsoRhoCorr")

        #if run != 251251 : continue

        if photons.size() > 0 and HT > 500.: 
            for p in range( photons.size() ) : 
                if isEB[p]==1. and hOverE[p] < 0.028 and photons[p].Pt() > 100. and pixelSeed[p] == 0:
                    if charIso[p] < 2.67 and photIso[p] < ( 2.11 + 0.0014*photons[p].Pt() ) and neutIso[p] < ( 7.23 + exp(0.0028*photons[p].Pt()+0.5408) ) :  
                        if maxEvents != -1 :
                            histo_.Fill(photons[p].Pt(),sample.weight*numEvents/maxEvents)
                        else :
                            histo_.Fill(photons[p].Pt(),sample.weight)
                        
    return histo_

sampleListMC = [ "Gjets400" , "Gjets600" ] #, "QCD500ext1" , "QCD1000ext1" ]
histoMC = {}

first = True

for s in samples :

    if not s.tag in sampleListMC : continue 

    histoMC[s] = plotHisto(s,100000)
    histoMC[s].SetFillColor(s.color)
    histoMC[s].SetLineColor(s.color)
    histoMC[s].GetXaxis().SetNdivisions(505)
    histoMC[s].Scale(lumi)
    if first :
        totalMC = TH1F(histoMC[s])
        totalMC.SetName("totalMC")
        first=False
    else :
        totalMC.Add(histoMC[s])
        
sampleListData = [ "SinglePhoton" ]
histoData = {}

first = True

for s in dataSamples :

    if not s.tag in sampleListData : continue 

    histoData[s] = plotHisto(s,-1)
    histoData[s].SetMarkerStyle(8)
    histoData[s].GetXaxis().SetNdivisions(505)
    if first : 
        totalData = TH1F(histoData[s])
        totalData.SetName("totalData")
        first=False
    else : 
        totalData.Add(histoData[s])

totalMC.Scale(totalData.Integral()/totalMC.Integral())

totalData.Draw("p,e1")
totalMC.Draw("SAME,HIST")
totalData.Draw("SAME,p,e1")

leg = TLegend(.6,.6,.9,.9)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(totalMC,"MC","f")
leg.AddEntry(totalData,"Data","p")
leg.Draw()

setLumi(lumi)
CMSlabel.Draw()
SqrtSlumi.Draw()
