from ROOT import *
from math import *
from inputFiles import *
from photonUtils import *
from triggerUtils import *
from RA2Utils import *
from array import *

def plotNminusOneHisto( sample , maxEvents ) :

    histo_ = {}

    histoTemplate = {}
    histoTemplate["sieie"] =  TH1F("sieie",";#sigma_{i#etai#eta};Events",60,0,0.03)
    histoTemplate["HoverE"] =  TH1F("H/E",";H/E;Events",60,0,0.1)
    histoTemplate["charIso"] =  TH1F("charIso",";Charged Isolation;Events",60,0,10)
    histoTemplate["photIso"] =  TH1F("photIso",";Photon Isolation;Events",60,0,10)
    histoTemplate["neutIso"] =  TH1F("neutIso",";Neutral Had. Isolation;Events",60,0,10)
    histoTemplate["pt"] = TH1F("pt",";p_{T,#gamma} [GeV];Events",20,100.,500.)
    histoTemplate["pixelSeed"] = TH1F("pixelSeed",";Pixel Seed;Events",2,-0.5,1.5)

    photonCuts = {}
    photonVars = {}

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
        NumPhotons = getattr( sample.tree , "NumPhotons" )
        photon.getBranches( iEvt )
        trigger.getBranches( iEvt )

        if NumPhotons > 1 : continue

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
                    
                    passCuts = True
                    for cut in photonCuts[key] : 
                        if not cut( p ) : passCuts = False 
                        
                    if passCuts : 
                        if maxEvents != -1 :
                            histo_[key].Fill(photonVars[key],sample.weight*numEvents/maxEvents)
                        else :
                            histo_[key].Fill(photonVars[key],sample.weight)
                        
    return histo_

def plotDrellYanCRHisto( sample , maxEvents ) :

    histo_ = {}

    MHTbinning = array('f',[200,250,350,500,1000])
    MHTLoosebinning = array('f',[125,200,350,500,1000])
    HTbinning = array('f',[500,600,800,1200])
    HTLoosebinning = array('f',[400,550,800,1200])
    NJetsbinning = array('f',[4.,7.,9.,12.])
    BTagsbinning = array('f',[-0.5,0.5,1.5,3.5])
    BTagsLoosebinning = array('f',[-0.5,0.5,1.5,3.5])

    histo_["HT"] = TH1F("HTclean",";H_{T} [GeV];Events",20,400.,1000.)
    histo_["HT"].SetName(sample.tag+"_HT")
    histo_["HTLoose"] = TH1F("HTclean",";H_{T} [GeV];Events",len(HTLoosebinning)-1,HTLoosebinning)
    histo_["HTLoose"].SetName(sample.tag+"_HTLoose")
    histo_["HTcustBin"] = TH1F("HTclean_custBin",";H_{T} [GeV];Events",len(HTbinning)-1,HTbinning)
    histo_["HTcustBin"].SetName(sample.tag+"_HTcustBin")
    histo_["MHT"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",20,100.,700.)
    histo_["MHT"].SetName(sample.tag+"_MHT")
    histo_["MHTLoose"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",len(MHTLoosebinning)-1,MHTLoosebinning)
    histo_["MHTLoose"].SetName(sample.tag+"_MHTLoose")
    histo_["MHTcustBin"] = TH1F("MHTcustBin",";H^{miss}_{T} [GeV];Events",len(MHTbinning)-1,MHTbinning)
    histo_["MHTcustBin"].SetName(sample.tag+"_MHTcustBin")
    histo_["NJetsLoose"] = TH1F("NJetsclean",";N_{jets};Events",7,.5,7.5)
    histo_["NJetsLoose"].SetName(sample.tag+"_NJetsLoose")
    histo_["NJetscustBin"] = TH1F("NJetsclean_custBin",";N_{jets};Events",len(NJetsbinning)-1,NJetsbinning)
    histo_["NJetscustBin"].SetName(sample.tag+"_NJetscustBin")
    histo_["BTags"] = TH1F("BTagsclean",";N_{b-jets} ;Events",4,-0.5,3.5)
    histo_["BTags"].SetName(sample.tag+"_BTags")
    histo_["BTagsLoose"] = TH1F("BTagsclean",";N_{b-jets} ;Events",len(BTagsLoosebinning)-1,BTagsLoosebinning)
    histo_["BTagsLoose"].SetName(sample.tag+"_BTagsLoose")
    histo_["BTagscustBin"] = TH1F("BTagsclean_custBin",";N_{b-jets} ;Events",len(BTagsbinning)-1,BTagsbinning)
    histo_["BTagscustBin"].SetName(sample.tag+"_BTagscustBin")
    histo_["DeltaPhi1"] = TH1F("DeltaPhi1",";#Delta#phi_{1} ;Events",10,0.,3.1415)
    histo_["DeltaPhi1"].SetName(sample.tag+"_DeltaPhi1")
    histo_["DeltaPhi2"] = TH1F("DeltaPhi2",";#Delta#phi_{2} ;Events",10,0.,3.1415)
    histo_["DeltaPhi2"].SetName(sample.tag+"_DeltaPhi2")
    histo_["DeltaPhi3"] = TH1F("DeltaPhi3",";#Delta#phi_{3} ;Events",10,0.,3.1415)
    histo_["DeltaPhi3"].SetName(sample.tag+"_DeltaPhi3")

    histo_["Mll_allPt"] = TH1F(sample.tag+"_Mll_allPt",";m_{#l#l} [GeV];Events",20,10,210)
    histo_["Zpt"] = TH1F(sample.tag+"Zpt",";p_{T,Z} [GeV];Events",20,10,400)
    histo_["Zeta"] = TH1F(sample.tag+"Zeta",";#eta_{Z} [GeV];Events",20,-5,5)
    
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
                    histo_["MHTcustBin"].Fill(RA2.MHTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["MHT"].Fill(RA2.MHTclean,sample.weight)
                    histo_["MHTcustBin"].Fill(RA2.MHTclean,sample.weight)
                    
            if RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["HT"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                    histo_["HTcustBin"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["HT"].Fill(RA2.HTclean,sample.weight)
                    histo_["HTcustBin"].Fill(RA2.HTclean,sample.weight)
                    
            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["NJetscustBin"].Fill(RA2.NJetsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["NJetscustBin"].Fill(RA2.NJetsclean,sample.weight)

            if RA2.HTclean > 400. and RA2.MHTclean > 125. and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["NJetsLoose"].Fill(RA2.NJetsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["NJetsLoose"].Fill(RA2.NJetsclean,sample.weight)

                if maxEvents != -1 :
                    histo_["MHTLoose"].Fill(RA2.MHTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["MHTLoose"].Fill(RA2.MHTclean,sample.weight)

                if maxEvents != -1 :
                    histo_["BTagsLoose"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["BTagsLoose"].Fill(RA2.BTagsclean,sample.weight)

                if maxEvents != -1 :
                    histo_["HTLoose"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["HTLoose"].Fill(RA2.HTclean,sample.weight)

            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["BTags"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                    histo_["BTagscustBin"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["BTags"].Fill(RA2.BTagsclean,sample.weight)
                    histo_["BTagscustBin"].Fill(RA2.BTagsclean,sample.weight)

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

    MHTbinning = array('f',[200,250,350,500,1000])
    MHTLoosebinning = array('f',[125,200,350,500,1000])
    HTbinning = array('f',[500,600,800,1200])
    HTLoosebinning = array('f',[400,550,800,1200])
    NJetsbinning = array('f',[4.,7.,9.,12.])
    BTagsbinning = array('f',[-0.5,0.5,1.5,3.5])
    BTagsLoosebinning = array('f',[-0.5,0.5,1.5,3.5])

    histo_["HT"] = TH1F("HTclean",";H_{T} [GeV];Events",20,400.,1000.)
    histo_["HT"].SetName(sample.tag+"_HT")
    histo_["HTLoose"] = TH1F("HTclean",";H_{T} [GeV];Events",len(HTLoosebinning)-1,HTLoosebinning)
    histo_["HTLoose"].SetName(sample.tag+"_HTLoose")
    histo_["HTcustBin"] = TH1F("HTclean_custBin",";H_{T} [GeV];Events",len(HTbinning)-1,HTbinning)
    histo_["HTcustBin"].SetName(sample.tag+"_HTcustBin")
    histo_["MHT"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",20,100.,700.)
    histo_["MHT"].SetName(sample.tag+"_MHT")
    histo_["MHTLoose"] = TH1F("MHT",";H^{miss}_{T} [GeV];Events",len(MHTLoosebinning)-1,MHTLoosebinning)
    histo_["MHTLoose"].SetName(sample.tag+"_MHTLoose")
    histo_["MHTcustBin"] = TH1F("MHTcustBin",";H^{miss}_{T} [GeV];Events",len(MHTbinning)-1,MHTbinning)
    histo_["MHTcustBin"].SetName(sample.tag+"_MHTcustBin")
    histo_["NJetsLoose"] = TH1F("NJetsclean",";N_{jets};Events",7,.5,7.5)
    histo_["NJetsLoose"].SetName(sample.tag+"_NJetsLoose")
    histo_["NJetscustBin"] = TH1F("NJetsclean_custBin",";N_{jets};Events",len(NJetsbinning)-1,NJetsbinning)
    histo_["NJetscustBin"].SetName(sample.tag+"_NJetscustBin")
    histo_["BTags"] = TH1F("BTagsclean",";N_{b-jets} ;Events",4,-0.5,3.5)
    histo_["BTags"].SetName(sample.tag+"_BTags")
    histo_["BTagsLoose"] = TH1F("BTagsclean",";N_{b-jets} ;Events",len(BTagsLoosebinning)-1,BTagsLoosebinning)
    histo_["BTagsLoose"].SetName(sample.tag+"_BTagsLoose")
    histo_["BTagscustBin"] = TH1F("BTagsclean_custBin",";N_{b-jets} ;Events",len(BTagsbinning)-1,BTagsbinning)
    histo_["BTagscustBin"].SetName(sample.tag+"_BTagscustBin")
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
                    histo_["MHTcustBin"].Fill(RA2.MHTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["MHT"].Fill(RA2.MHTclean,sample.weight)
                    histo_["MHTcustBin"].Fill(RA2.MHTclean,sample.weight)
                    
            if RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["HT"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                    histo_["HTcustBin"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["HT"].Fill(RA2.HTclean,sample.weight)
                    histo_["HTcustBin"].Fill(RA2.HTclean,sample.weight)
                    
            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["NJetscustBin"].Fill(RA2.NJetsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["NJetscustBin"].Fill(RA2.NJetsclean,sample.weight)

            if RA2.HTclean > 400. and RA2.MHTclean > 125. and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["NJetsLoose"].Fill(RA2.NJetsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["NJetsLoose"].Fill(RA2.NJetsclean,sample.weight)

                if maxEvents != -1 :
                    histo_["MHTLoose"].Fill(RA2.MHTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["MHTLoose"].Fill(RA2.MHTclean,sample.weight)

                if maxEvents != -1 :
                    histo_["BTagsLoose"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["BTagsLoose"].Fill(RA2.BTagsclean,sample.weight)

                if maxEvents != -1 :
                    histo_["HTLoose"].Fill(RA2.HTclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["HTLoose"].Fill(RA2.HTclean,sample.weight)


            if RA2.HTclean > 500. and RA2.MHTclean > 200. and RA2.NJetsclean > 3 and RA2.DeltaPhi1clean > 0.5 and RA2.DeltaPhi2clean > 0.5 and RA2.DeltaPhi3clean > 0.3 : 
                if maxEvents != -1 :
                    histo_["BTags"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                    histo_["BTagscustBin"].Fill(RA2.BTagsclean,sample.weight*numEvents/maxEvents)
                else :
                    histo_["BTags"].Fill(RA2.BTagsclean,sample.weight)
                    histo_["BTagscustBin"].Fill(RA2.BTagsclean,sample.weight)

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
