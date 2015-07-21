from ROOT import *
from math import *

class photonUtil : 
    
    def __init__( self , tree ) :

        self.tree = tree 

        self.fourVec = None
        self.hOverE = None
        self.sieie = None
        self.isEB = None
        self.pixelSeed = None
        self.eleVeto = None
        self.photIso = None
        self.neutIso = None
        self.charIso = None
        self.vars = { "hOverE":self.hOverE,
                      "sieie" :self.sieie ,
                      "isEB"  :self.isEB  ,
                      "pixelSeed":self.pixelSeed,
                      "eleVeto":self.eleVeto,
                      "photIso":self.photIso,
                      "neutIso":self.neutIso,
                      "charIso":self.charIso
                      }

    def getBranches( self , iEvent , debug = False ) : 

        self.tree.GetEntry( iEvent )

        self.fourVec = getattr(self.tree,"photonCands")
        self.hOverE = getattr(self.tree,"photon_hadTowOverEM")
        self.sieie = getattr(self.tree,"photon_sigmaIetaIeta")
        self.isEB = getattr(self.tree,"photon_isEB")
        self.pixelSeed = getattr(self.tree,"photon_hasPixelSeed")
        self.eleVeto = getattr(self.tree,"photon_hasPixelSeed")
        self.photIso = getattr(self.tree,"photon_pfGammaIsoRhoCorr")
        self.neutIso = getattr(self.tree,"photon_pfNeutralIsoRhoCorr")
        self.charIso = getattr(self.tree,"photon_pfChargedIsoRhoCorr")

        if debug :
            self.dump()

    def dump( self ):

        for p in range( len( self.fourVec ) ) :
            print "-----",str(p)+"th photon -----"
            ## note vars is a dictionary, so var is the keys
            print "pt",self.fourVec[p].Pt()
            print "sieie",self.sieie[p]
            print "hOverE",self.hOverE[p]
            print "isEB",self.isEB[p]
            print "pixelSeed",self.pixelSeed[p]
            print "eleVeto",self.eleVeto[p]
            print "photIso",self.photIso[p]
            print "neutIso",self.neutIso[p]
            print "charIso",self.charIso[p]

    def passPt( self , p ) : 
        
        return self.fourVec[p].Pt() > 100. 

    def passPixelSeed( self , p ) :
        
        return self.pixelSeed[p] == 1. 

    def passHoverE( self , p ) : 
            
        if self.isEB[p] == 1. : 
            return self.hOverE[p] < 0.028
        else : 
            return self.hOverE[p] < 0.093

    def passSieie( self , p ) : 
            
        if self.isEB[p] == 1. : 
            return self.sieie[p] < 0.0107
        else : 
            return self.hOverE[p] < 0.0272
        
    def passCharIso( self , p ) : 

        if self.isEB[p] == 1. :
            return self.charIso[p] < 2.67
        else :
            return self.charIso[p] < 1.79

    def passNeutIso( self , p ) : 
        
        if self.isEB[p] == 1. : 
            return self.neutIso[p] < 7.23 + exp(0.0028*self.fourVec[p].Pt()+0.5408)
        else : 
            return self.neutIso[p] < 8.89 + 0.01725*self.fourVec[p].Pt()

    def passPhotIso( self , p ) :

        if self.isEB[p] == 1. : 
            return self.photIso < 2.11 + 0.0014*self.fourVec[p].Pt()
        else : 
            return self.photIso < 3.09 + 0.0091*self.fourVec[p].Pt() 


