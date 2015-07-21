from ROOT import *
from math import *
from inputFiles import *
from photonUtils import *
from triggerUtils import *
from RA2Utils import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

def plotDrellYanCRHisto( sample , maxEvents ) :

    histo_ = {}

    histo_["HT"] = TH1F("HTclean",";H_{T} [GeV];Events",20,400.,1000.)
    histo_["HT"].SetName(sample.tag+"_HT")
    histo_["MHT"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",20,100.,700.)
    histo_["MHT"].SetName(sample.tag+"_MHT")
    histo_["NJets"] = TH1F("NJetsclean",";N_{jets};Events",6,3.5,9.5)
    histo_["NJets"].SetName(sample.tag+"_NJets")
    histo_["BTags"] = TH1F("BTagsclean",";N_{b-jets} ;Events",4,-0.5,3.5)
    histo_["BTags"].SetName(sample.tag+"_BTags")
    histo_["DeltaPhi1"] = TH1F("DeltaPhi1",";#Delta#phi_{1} ;Events",10,0.,3.1415)
    histo_["DeltaPhi1"].SetName(sample.tag+"_DeltaPhi1")
    histo_["DeltaPhi2"] = TH1F("DeltaPhi2",";#Delta#phi_{2} ;Events",10,0.,3.1415)
    histo_["DeltaPhi2"].SetName(sample.tag+"_DeltaPhi2")
    histo_["DeltaPhi3"] = TH1F("DeltaPhi3",";#Delta#phi_{3} ;Events",10,0.,3.1415)
    histo_["DeltaPhi3"].SetName(sample.tag+"_DeltaPhi3")

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

def plotPhotonCRHisto( sample , maxEvents ) :

    histo_ = {}
    histo_["HT"] = TH1F("HTclean",";H_{T} [GeV];Events",20,400.,1000.)
    histo_["HT"].SetName(sample.tag+"_HT")        
    histo_["MHT"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",20,100.,700.)
    histo_["MHT"].SetName(sample.tag+"_MHT")        
    histo_["NJets"] = TH1F("NJetsclean",";N_{jets};Events",6,3.5,9.5)
    histo_["NJets"].SetName(sample.tag+"_NJets")        
    histo_["BTags"] = TH1F("BTagsclean",";N_{b-jets} ;Events",4,-0.5,3.5)
    histo_["BTags"].SetName(sample.tag+"_BTags")        
    histo_["DeltaPhi1"] = TH1F("DeltaPhi1",";#Delta#phi_{1} ;Events",10,0.,3.1415)
    histo_["DeltaPhi1"].SetName(sample.tag+"_DeltaPhi1")        
    histo_["DeltaPhi2"] = TH1F("DeltaPhi2",";#Delta#phi_{2} ;Events",10,0.,3.1415)
    histo_["DeltaPhi2"].SetName(sample.tag+"_DeltaPhi2")        
    histo_["DeltaPhi3"] = TH1F("DeltaPhi3",";#Delta#phi_{3} ;Events",10,0.,3.1415)
    histo_["DeltaPhi3"].SetName(sample.tag+"_DeltaPhi3")

    numEvents = sample.tree.GetEntries()
    photon = photonUtil( sample.tree )
    trigger = triggerUtil( sample.tree )
    RA2 = RA2Util( sample.tree )

    for iEvt in range( numEvents ) : 

        if iEvt > maxEvents and maxEvents != -1 : break

        sample.tree.GetEntry(iEvt)
        HT = getattr( sample.tree , "HT" )

        photon.getBranches( iEvt )
        trigger.getBranches( iEvt )
        RA2.getBranches( iEvt )

        if iEvt % 10000 == 0 : 
            print "event:",iEvt

        if RA2.passPhotonCR() and trigger.result( "HLT_Photon90_CaloIdL_PFHT500" ) == 1 : 

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
