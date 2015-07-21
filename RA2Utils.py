from ROOT import *

class RA2Util :
    
    def __init__( self , tree ) :
        
        self.tree = tree
        self.HT = -999.
        self.HTclean = -999.
        self.MHT = -999.
        self.MHTclean = -999.
        self.NJets = -99
        self.NJetsclean = -99
        self.BTags = -99
        self.BTagsclean = -99
        self.DeltaPhi1 = -99.
        self.DeltaPhi1clean = -99.
        self.DeltaPhi2 = -99.
        self.DeltaPhi2clean = -99.
        self.DeltaPhi3 = -99.
        self.DeltaPhi3clean = -99.
        self.NumPhotons = -99
        self.Leptons = -99
        self.Zp4 = None
        self.JetID = None

    def getBranches( self , iEvt ) : 
        
        self.tree.GetEntry( iEvt )
        
        self.HT             = getattr( self.tree , "HT" )
        self.HTclean        = getattr( self.tree , "HTclean" )
        self.MHT            = getattr( self.tree , "MHT" )
        self.MHTclean       = getattr( self.tree , "MHTclean" )
        self.NJets          = getattr( self.tree , "NJets" )
        self.NJetsclean     = getattr( self.tree , "NJetsclean" )
        self.BTags          = getattr( self.tree , "BTags" )
        self.BTagsclean     = getattr( self.tree , "BTagsclean" )
        self.DeltaPhi1      = getattr( self.tree , "DeltaPhi1" )
        self.DeltaPhi1clean = getattr( self.tree , "DeltaPhi1clean" )
        self.DeltaPhi2      = getattr( self.tree , "DeltaPhi2" )
        self.DeltaPhi2clean = getattr( self.tree , "DeltaPhi2clean" )
        self.DeltaPhi3      = getattr( self.tree , "DeltaPhi3" )
        self.DeltaPhi3clean = getattr( self.tree , "DeltaPhi3clean" )
        
        self.Leptons        = getattr( self.tree , "Leptons" )
        self.NumPhotons     = getattr( self.tree , "NumPhotons" )
        self.JetID          = getattr( self.tree , "JetID" )
        self.Zp4            = getattr( self.tree , "Zp4" )
        
    def dump( self ) :
        
        print " - - - - - - - - - - - - - "
        print "HT",self.HT
        print "HTclean",self.HTclean
        print "MHT",self.MHT
        print "MHTclean",self.MHTclean
        print "NJets",self.NJets
        print "NJetsclean",self.NJetsclean
        print "BTags",self.BTags
        print "BTagsclean",self.BTagsclean
        print "DeltaPhi1",self.DeltaPhi1
        print "DeltaPhi1clean",self.DeltaPhi1clean
        print "DeltaPhi2",self.DeltaPhi2
        print "DeltaPhi2clean",self.DeltaPhi2clean
        print "DeltaPhi3",self.DeltaPhi3
        print "DeltaPhi3clean",self.DeltaPhi3clean
        print "Leptons",self.Leptons
        print "NumPhotons",self.NumPhotons
        print "JetID",self.JetID
        
    def passBaseline( self ) : 

        return self.HT > 500. and self.MHT > 200. and self.NJets > 3 and self.DeltaPhi1 > 0.5 and self.DeltaPhi2 > 0.5 and self.DeltaPhi3 > 0.5 and self.Leptons == 0 #and self.JetID == 1

    def passPhotonCR( self ) :
        
        return self.Leptons == 0 and self.NumPhotons == 1 #and self.JetID == 1 

    def passPhotonCRbaseline( self ) :
        
        return self.HTclean > 500. and self.MHTclean > 200. and self.NJetsclean > 3 and self.DeltaPhi1clean > 0.5 and self.DeltaPhi2clean > 0.5 and self.DeltaPhi3clean >0.5 and self.Leptons == 0 and self.NumPhotons == 1 #and self.JetID == 1 

    def passDrellYanCR( self ) : 

        return self.Zp4.size() == 1 and self.Zp4[0].M() > 75. and self.Zp4[0].M() < 115. # and self.JetID == 1

    def passDrellYanCRbaseline( self ) : 

        return self.HTclean > 500. and self.MHTclean > 200. and self.NJetsclean > 3 and self.DeltaPhi1clean > 0.5 and self.DeltaPhi2clean > 0.5 and self.DeltaPhi3clean >0.5 and self.Zp4.size() == 1 and self.Zp4[0].M() > 75. and self.Zp4[0].M() < 115. # and self.JetID == 1
