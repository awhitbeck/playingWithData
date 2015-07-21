from ROOT import *
from labels import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

tree = TChain("TreeMaker2/PreSelection")
tree.Add("../PromptReco_RA2b_July13_2015/Run2015B-PromptReco-v1.DoubleMuon*.root")

histoZ = TH1F("Zmass",";m_{#mu^{+}#mu^{-}};Events / 2. GeV",30,50,110)
histoZgam = TH1F("ZgammaMass",";m_{#mu^{+}#mu^{-}#gamma};Events / 2. GeV",30,50,110)
histo2D = TH2F("histo2D",";m_{#mu^{+}#mu^{-}#gamma};m_{#mu^{+}#mu^{-}}",30,50,110,30,50,110)

for iEvt in range( tree.GetEntries() ) : 

    tree.GetEntry(iEvt)

    muon = getattr(tree,"Muons")
    muonCharge = getattr(tree,"MuonCharge")
    run = getattr(tree,"RunNum")
    photons = getattr(tree,"photonCands")
    hOverE = getattr(tree,"photon_hadTowOverEM")
    sieie = getattr(tree,"photon_sigmaIetaIeta")
    isEB = getattr(tree,"photon_isEB")

    #if run != 251251 : continue
    # check for two oppositely charged muons

    if muon.size() == 2 and photons.size() > 0 :

        if muonCharge[0] + muonCharge[1] != 0 : continue

        Z = muon[0] + muon[1]

        for p in range(photons.size()) : 
            if isEB[p]==1. and hOverE[p] < 0.028 and photons[p].Pt() > 10. :
                histoZgam.Fill((Z+photons[p]).M())
                histo2D.Fill((Z+photons[p]).M(),Z.M())

#histoZ.SetMarkerStyle(8)
#histoZgam.SetMarkerStyle(8)
#histoZgam.Draw("p,e1")           
histo2D.Draw("colz")

setLumi(0.006)            
CMSlabel.Draw()
SqrtSlumi.Draw()
