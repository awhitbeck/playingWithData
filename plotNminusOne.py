from ROOT import *
from labels import *
from math import *
from inputFiles import *
from photonUtils import *
from triggerUtils import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

histoTemplate = {}
histoTemplate["sieie"] =  TH1F("sieie",";#sigma_{i#etai#eta};Events",60,0,0.03)
histoTemplate["HoverE"] =  TH1F("H/E",";H/E;Events",60,0,0.1)
histoTemplate["charIso"] =  TH1F("charIso",";Charged Isolation;Events",60,0,10)
histoTemplate["photIso"] =  TH1F("photIso",";Photon Isolation;Events",60,0,10)
histoTemplate["neutIso"] =  TH1F("neutIso",";Neutral Had. Isolation;Events",60,0,10)
histoTemplate["pt"] = TH1F("pt",";p_{T,#gamma} [GeV];Events",50,100.,500.)
histoTemplate["pixelSeed"] = TH1F("pixelSeed",";Pixel Seed;Events",2,-0.5,1.5)

lumi = 0.0492

photonCuts = {}
photonVars = {}

def plotHisto( sample , maxEvents ) :

    histo_ = {}

    for key in histoTemplate : 
        histo_[key] = TH1F( histoTemplate[key] )
        histo_[key].SetName(sample.tag+"_"+key)

    numEvents = sample.tree.GetEntries()
    photon = photonUtil( sample.tree )
    trigger = triggerUtil( sample.tree )

    photonCuts["sieie"] = [ photon.passPt , photon.passCharIso , photon.passNeutIso , photon.passPhotIso , photon.passHoverE , photon.passPixelSeed ]
    photonCuts["HoverE"] = [ photon.passPt , photon.passCharIso , photon.passNeutIso , photon.passPhotIso , photon.passSieie , photon.passPixelSeed ]
    photonCuts["charIso"] = [ photon.passPt , photon.passSieie , photon.passNeutIso , photon.passPhotIso , photon.passHoverE , photon.passPixelSeed ]
    photonCuts["neutIso"] = [ photon.passPt , photon.passCharIso , photon.passSieie , photon.passPhotIso , photon.passHoverE , photon.passPixelSeed ]
    photonCuts["photIso"] = [ photon.passPt , photon.passCharIso , photon.passNeutIso , photon.passSieie , photon.passHoverE , photon.passPixelSeed ]
    photonCuts["pixelSeed"] = [ photon.passPt , photon.passCharIso , photon.passNeutIso , photon.passPhotIso , photon.passHoverE , photon.passSieie ]
    photonCuts["pt"] = [ photon.passSieie , photon.passCharIso , photon.passNeutIso , photon.passPhotIso , photon.passHoverE , photon.passPixelSeed ]

    for iEvt in range( numEvents ) : 

        if iEvt > maxEvents and maxEvents != -1 : break

        sample.tree.GetEntry(iEvt)
        HT = getattr( sample.tree , "HT" )

        photon.getBranches( iEvt )
        trigger.getBranches( iEvt )

        if iEvt % 10000 == 0 : 
            print "event:",iEvt

        if photon.fourVec.size() > 0 and HT > 500. and trigger.result( "HLT_Photon90_CaloIdL_PFHT500" ) == 1 : 
            for p in range( len( photon.fourVec ) ) : 

                photonVars["charIso"] = photon.charIso[p]
                photonVars["neutIso"] = photon.neutIso[p]
                photonVars["photIso"] = photon.photIso[p]
                photonVars["pixelSeed"] = photon.pixelSeed[p]
                photonVars["HoverE"] = photon.hOverE[p]
                photonVars["sieie"] = photon.sieie[p]
                photonVars["pt"] = photon.fourVec[p].Pt()
                
                ##### only plot barrel photons #####
                if photon.isEB[p] != 1. : continue

                ################# loop over different cut combinations #####################
                for key in photonCuts : 
                    for cut in photonCuts[key] : 
                        if not cut( p ) : break 
                        
                        #print key,photonVars[key]

                        if maxEvents != -1 :
                            histo_[key].Fill(photonVars[key],sample.weight*numEvents/maxEvents)
                        else :
                            histo_[key].Fill(photonVars[key],sample.weight)
                        
    return histo_

sampleListMC = [ "Gjets400" , "Gjets600" ] #, "QCD500ext1" , "QCD1000ext1" ]
histoMC = {}
totalMC = {}

first = { "sieie" : True  , 
          "HoverE" : True ,
          "charIso" : True , 
          "photIso" : True , 
          "neutIso" : True ,
          "pt" : True ,
          "pixelSeed" : True }

for s in samples :

    if not s.tag in sampleListMC : continue 

    histoMC[s] = plotHisto(s,100000)
    for key in histoTemplate : 
        histoMC[s][key].SetFillColor(s.color)
        histoMC[s][key].SetLineColor(s.color)
        histoMC[s][key].GetXaxis().SetNdivisions(505)
        histoMC[s][key].Scale(lumi)
        if first[key] :
            print key
            totalMC[key] = TH1F(histoMC[s][key])
            totalMC[key].SetName("totalMC_"+key)
            first[key]=False
        else :
            print key
            totalMC[key].Add(histoMC[s][key])
        
sampleListData = [ "SinglePhoton" ]
histoData = {}
totalData = {}
first = { "sieie" : True  , 
          "HoverE" : True ,
          "charIso" : True , 
          "photIso" : True , 
          "neutIso" : True ,
          "pt" : True ,
          "pixelSeed" : True }

for s in dataSamples :

    if not s.tag in sampleListData : continue 

    histoData[s] = plotHisto(s,-1)
    for key in histoTemplate :
        histoData[s][key].SetMarkerStyle(8)
        histoData[s][key].GetXaxis().SetNdivisions(505)
        if first[key] : 
            totalData[key] = TH1F(histoData[s][key])
            totalData[key].SetName("totalData_"+key)
            first[key]=False
        else : 
            totalData[key].Add(histoData[s][key])

        totalMC[key].Scale(totalData[key].Integral()/totalMC[key].Integral())

can = {}

for key in histoTemplate : 
    can[key] = TCanvas("can_"+key,"can_"+key,500,500)
    totalMC[key].GetYaxis().SetRangeUser( 0. , max( [ totalMC[key].GetMaximum() , totalData[key].GetMaximum() ] )*1.3 )
    totalMC[key].Draw("HIST")
    totalData[key].Draw("SAME,p,e1")
    
    leg = TLegend(.6,.6,.9,.9)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.AddEntry(totalMC[key],"MC","f")
    leg.AddEntry(totalData[key],"Data","p")
    leg.Draw()

    setLumi(lumi)
    CMSlabel.Draw()
    SqrtSlumi.Draw()

    can[key].SaveAs("photonNminusOne_"+key+".eps")
    can[key].SaveAs("photonNminusOne_"+key+".png")
    can[key].SaveAs("photonNminusOne_"+key+".pdf")
