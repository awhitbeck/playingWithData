from os import walk,system
from ROOT import *
import subprocess

eosDir = "/eos/uscms"
redirector = "root://cmsxrootd.fnal.gov//"
baseDir = "/store/user/lpcsusyhad/SusyRA2Analysis2015/FinalProductionDPS/"
lumi = 10000

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

class sampleInfo : 


    def __init__( self , fileName , tag , color , xsec , weight=1. , legendLabel="" ) :
        self.fileName = fileName 
        self.color    = color
        self.xsec     = xsec
        self.tag      = tag
        self.inputFile= None
        self.tree = TChain("TreeMaker2/PreSelection")
        self.weight   = weight
        self.legendLabel = legendLabel
        self.addToChain()

    def addToChain( self ):

        #proc = subprocess.Popen( [ "ls /eos/uscms/{0}".format( self.fileName ) ] , stdout = subprocess.PIPE , shell = True )
        #( files , errors ) = proc.communicate()
        files = open("fileList.txt")
        
        for f in files.read().split("\n") : 

            if f.find(self.fileName) != -1 : 
                f = redirector+f
                #print f
                self.tree.Add( "{0}".format( f ) )

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
dataSamples = [ sampleInfo( "Run2015B-PromptReco-v1.SinglePhoton"   , "SinglePhoton"   , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-17Jul2015-v1.SinglePhoton"    , "SinglePh17July"   , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-PromptReco-v1.DoubleMuon"     , "DoubleMuon"     , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-17Jul2015-v1.DoubleMuon"      , "DoubleMuon17July"     , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-PromptReco-v1.DoubleEG"       , "DoubleElectron" , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-17Jul2015-v1.DoubleEG"        , "DoubleElectron17July" , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-PromptReco-v1.SingleElectron" , "SingleElectron" , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-17Jul2015-v1.SingleElectron"  , "SingleElectron17July" , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-PromptReco-v1.SingleMuon"     , "SingleMuon"     , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-17Jul2015-v1.SingleMuon"      , "SingleMuon17July"     , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-PromptReco-v1.HTMHT"          , "HTMHT"          , 1 , 1. , 1. , "Data" ) ,
                sampleInfo( "Run2015B-17Jul2015-v1.HTMHT"           , "HTMHT17July"          , 1 , 1. , 1. , "Data" )
                ]

samples = [ sampleInfo( "Spring15.GJets_HT-400To600"           ,  "Gjets400"  , kRed+1     , 273.    , 0.132 , "#gamma+jets" ) , 
            sampleInfo( "Spring15.GJets_HT-600ToInf"           ,  "Gjets600"  , kRed+1     , 94.5    , 0.0379 , "#gamma+jets" ) ,
            sampleInfo( "Spring15.ZJetsToNuNu_HT-600ToInf"     ,  "Zinv400"   , kRed+2     , 10.94   , 0.0117 , "Z(#nu#nu)+jets" ) ,
            sampleInfo( "Spring15.ZJetsToNuNu_HT-400To600"     ,  "Zinv600"   , kRed+2     , 4.203   , 0.00414 , "Z(#nu#nu)+jets" ) ,
            sampleInfo( "Spring15.DYJetsToLL_M-50_HT-400to600" ,  "DYJets400" , kMagenta   , 6.761   , 0.00744 , "Drell-Yan+jets" ) ,
            sampleInfo( "Spring15.DYJetsToLL_M-50_HT-600toInf" ,  "DYJets600" , kMagenta   , 2.718   , 0.000810 , "Drell-Yan+jets" ) ,
            sampleInfo( "Spring15.QCD_Pt_80to120"              ,  "QCDpt80"   , kGreen+2   , 2762530 , 830.8 , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_120to170"             ,  "QCDpt120"  , kGreen+2   , 471100 , 140.5  , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_170to300"             ,  "QCDpt170"  , kGreen+2   , 117276 , 34.9   , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_300to470"             ,  "QCDpt300"  , kGreen+2   , 7823   , 2.70   , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_470to600"             ,  "QCDpt470"  , kGreen+2   , 648.2  , 0.335  , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_600to800"             ,  "QCDpt600"  , kGreen+2   , 186.9  , 0.100  , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_800to1000"            ,  "QCDpt800"  , kGreen+2   , 32.293 , 0.0174 , "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_1000to1400"           ,  "QCDpt1000" , kGreen+2   , 9.4183 , 0.00635, "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_1400to1800"           ,  "QCDpt1400" , kGreen+2   , 0.84265, 0.00431, "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_1800to2400"           ,  "QCDpt1800" , kGreen+2   , 0.114943, 0.000594, "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_2400to3200"           ,  "QCDpt2400" , kGreen+2   , 0.00682981, 3.51e-5, "QCD" ) ,
            sampleInfo( "Spring15.QCD_Pt_3200toInf"            ,  "QCDpt3200" , kGreen+2   , 0.000165445, 8.84e-7, "QCD" ) ,
            sampleInfo( "Spring15.TTJets_TuneCUETP8M1_13TeV"   ,  "TTJets"    , kCyan      , 806.1  , 0.0740   , "t#bar{t}" ) ,
            sampleInfo( "Spring15.WJetsToLNu_HT-400To600"      ,  "WJets400"  , kOrange-3  , 68.40  , 0.0325   , "W+jets" ) ,
            sampleInfo( "Spring15.WJetsToLNu_HT-600ToInf"      ,  "WJets600"  , kOrange-3  , 23.14  , 0.0222   , "W+jets" ) ,
            #sampleInfo( "PHYS14.SMS-T1bbbb_2J_mGl-1000_mLSP-900" ,  "T1bbbb_1000-900" , kMagenta+1 , 1.0 , 1.0 , "T1bbbb"        ) ,
            #sampleInfo( "PHYS14.SMS-T1bbbb_2J_mGl-1500_mLSP-100" ,  "T1bbbb_1500-100" , kMagenta+1 , 1.0 , 1.0 , "T1bbbb (Comp)" ) ,
            #sampleInfo( "PHYS14.SMS-T1qqqq_2J_mGl-1000_mLSP-800" ,  "T1qqqq_1000-800" , kMagenta+1 , 1.0 , 1.0 , "T1qqqq"        ) ,
            #sampleInfo( "PHYS14.SMS-T1qqqq_2J_mGl-1400_mLSP-100" ,  "T1qqqq_1500-100" , kMagenta+1 , 1.0 , 1.0 , "T1qqqq (Comp)" ) ,
            #sampleInfo( "PHYS14.SMS-T1tttt_2J_mGl-1200_mLSP-800" ,  "T1tttt_1200-800" , kMagenta+1 , 1.0 , 1.0 , "T1tttt"        ) ,
            #sampleInfo( "PHYS14.SMS-T1tttt_2J_mGl-1500_mLSP-100" ,  "T1tttt_1500-100" , kMagenta+1 , 1.0 , 1.0 , "T1tttt (Comp)" )
            ]

