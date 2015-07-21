from ROOT import *
from labels import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

tree = TChain("TreeMaker2/PreSelection")
tree.Add("../PromptReco_RA2b_July13_2015/Run2015B-PromptReco-v1.DoubleMuon*.root")

histo = TH1F("Zmass",";m_{#mu^{+}#mu^{-}};Events / 2. GeV",30,50,110)

for iEvt in range( tree.GetEntries() ) : 

    tree.GetEntry(iEvt)

    muon = getattr(tree,"Muons")
    muonCharge = getattr(tree,"MuonCharge")
    run = getattr(tree,"RunNum")
    if run != 251251 : continue
    # check for two oppositely charged muons
    if muon.size() == 2 : 
        if muonCharge[0] + muonCharge[1] == 0 :
            
            Z = muon[0] + muon[1]

            histo.Fill(Z.M())

histo.SetMarkerStyle(8)
histo.Draw("p,e1")
            
setLumi(0.006)            
CMSlabel.Draw()
SqrtSlumi.Draw()
