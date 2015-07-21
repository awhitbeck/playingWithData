from ROOT import *

class triggerUtil :
    
    def __init__( self , tree ) :
        
        self.tree = tree
        self.names = None
        self.passed = None

    def getBranches( self , iEvt ) :
        
        self.tree.GetEntry( iEvt )
        self.names = getattr( self.tree , "TriggerNames" )
        self.passed = getattr( self.tree , "PassTrigger" )

    def dump( self ) :
        
        for t in range( self.names.size() ) : 
            print self.names[t],self.passed[t]

    def result( self , trig ) : 

        for t in range( self.names.size() ) : 
            if self.names[t].find(trig) == -1  : continue
            return self.passed[ t ]

        return -1
