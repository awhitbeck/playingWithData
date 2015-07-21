from ROOT import *
from labels import *
from math import *
from inputFiles import *
from photonUtils import *
from triggerUtils import *
from RA2Utils import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

histoTemplate = {}
histoTemplate["HT"] = TH1F("HTclean",";H_{T} [GeV];Events",20,400.,1000.)
histoTemplate["MHT"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",20,100.,700.)
histoTemplate["NJets"] = TH1F("NJetsclean",";N_{jets};Events",6,3.5,9.5)
histoTemplate["BTags"] = TH1F("BTagsclean",";N_{b-jets} ;Events",4,-0.5,3.5)
histoTemplate["DeltaPhi1"] = TH1F("DeltaPhi1",";#Delta#phi_{1} ;Events",10,0.,3.1415)
histoTemplate["DeltaPhi2"] = TH1F("DeltaPhi2",";#Delta#phi_{2} ;Events",10,0.,3.1415)
histoTemplate["DeltaPhi3"] = TH1F("DeltaPhi3",";#Delta#phi_{3} ;Events",10,0.,3.1415)

lumi = 0.0492

def plotHisto( sample , maxEvents ) :

    histo_ = {}

    for key in histoTemplate : 
        histo_[key] = TH1F( histoTemplate[key] )
        histo_[key].SetName(sample.tag+"_"+key)

    numEvents = sample.tree.GetEntries()
    photon = photonUtil( sample.tree )
    trigger = triggerUtil( sample.tree )
    RA2 = RA2Util( sample.tree )

    for iEvt in range( numEvents ) : 

        if iEvt > maxEvents and maxEvents != -1 : break

        sample.tree.GetEntry(iEvt)

        photon.getBranches( iEvt )
        trigger.getBranches( iEvt )
        RA2.getBranches( iEvt )

        if iEvt % 10000 == 0 : 
            print "event:",iEvt

        #print RA2.passDrellYanCR(), trigger.result( "HLT_DoubleMu" ), trigger.result( "HLT_DoubeEle" )

        if RA2.passDrellYanCR() : #and ( trigger.result( "HLT_DoubleMu" ) or trigger.result( "HLT_DoubeEle" ) ) == 1 : 

            #print "HT",RA2.HTclean
            #print "MHT",RA2.MHTclean
            #print "NJets",RA2.NJetsclean
            #print "BTags",RA2.BTagsclean
            #print "DeltaPhi1",RA2.DeltaPhi1clean
            #print "DeltaPhi2",RA2.DeltaPhi2clean
            #print "DeltaPhi3",RA2.DeltaPhi3clean

            if RA2.HTclean > 500. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["MHT"].Fill(RA2.MHTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["MHT"].Fill(RA2.MHTclean,sample.weight)
                    
            if RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["HT"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["HT"].Fill(RA2.HTclean,sample.weight)
                    
            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["NJets"].Fill(RA2.NJetsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["NJets"].Fill(RA2.NJetsclean,sample.weight)

            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["BTags"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["BTags"].Fill(RA2.BTagsclean,sample.weight)

            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["DeltaPhi1"].Fill(RA2.DeltaPhi1clean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["DeltaPhi1"].Fill(RA2.DeltaPhi1clean,sample.weight)
                    
            if RA2.HTclean > 500. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["DeltaPhi2"].Fill(RA2.DeltaPhi2clean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["DeltaPhi2"].Fill(RA2.DeltaPhi2clean,sample.weight)

            if RA2.HTclean > 500. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 : 
                if maxEvents != -1 :
                    histo_["DeltaPhi3"].Fill(RA2.DeltaPhi3clean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["DeltaPhi3"].Fill(RA2.DeltaPhi3clean,sample.weight)
                    
    return histo_

outFile = TFile("drellYanCRkin.root","RECREATE")

sampleListMC = [ "DYJets400" , "DYJets600" ] #, "QCD500ext1" , "QCD1000ext1" ]
histoMC = {}
totalMC = {}
first = { "HT" : True  , 
          "MHT" : True ,
          "NJets" : True , 
          "BTags" : True , 
          "DeltaPhi1" : True ,
          "DeltaPhi2" : True ,
          "DeltaPhi3" : True }

for s in samples :

    if not s.tag in sampleListMC : continue 

    histoMC[s] = plotHisto(s,-1)
    for key in histoTemplate : 
        histoMC[s][key].SetFillColor(s.color)
        histoMC[s][key].SetLineColor(s.color)
        histoMC[s][key].GetXaxis().SetNdivisions(505)
        histoMC[s][key].Scale(lumi)
        histoMC[s][key].Write()
        if first[key] :
            print key
            totalMC[key] = TH1F(histoMC[s][key])
            totalMC[key].SetName("totalMC_"+key)
            first[key]=False
        else :
            print key
            totalMC[key].Add(histoMC[s][key])
        
sampleListData = [ "DoubleMuon", "DoubleElectron" ]
histoData = {}
totalData = {}
first = { "HT" : True  , 
          "MHT" : True ,
          "NJets" : True , 
          "BTags" : True , 
          "DeltaPhi1" : True ,
          "DeltaPhi2" : True ,
          "DeltaPhi3" : True }

for s in dataSamples :

    if not s.tag in sampleListData : continue 

    histoData[s] = plotHisto(s,-1)
    for key in histoTemplate :
        histoData[s][key].SetMarkerStyle(8)
        histoData[s][key].GetXaxis().SetNdivisions(505)
        histoData[s][key].Write()
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

    can[key].SaveAs("drellYanCRkin_"+key+".eps")
    can[key].SaveAs("drellYanCRkin_"+key+".png")
    can[key].SaveAs("drellYanCRkin_"+key+".pdf")

outFile.Close()
