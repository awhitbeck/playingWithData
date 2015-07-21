from os import walk
from ROOT import *
import subprocess

eosDir = "/eos/uscms"
redirector = "root://cmsxrootd.fnal.gov//"
baseDir = "/store/user/awhitbe1/PHYS14productionV13/"
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

        proc = subprocess.Popen( [ "ls /eos/uscms/{0}".format( self.fileName ) ] , stdout = subprocess.PIPE , shell = True )
        ( files , errors ) = proc.communicate()
        for f in files.split("\n") : 
            if f.find("No such file or directory") == -1 : 
                f = redirector+f[11:]
            self.tree.Add( "{0}".format( f ) )

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
dataSamples = [ sampleInfo( "/store/user/awhitbe1/Run2015B-PromptReco_July17/Run2015B-PromptReco-v1.SinglePhoton*" , "SinglePhoton" , 1 , 1. , 1. , "Single-#gamma dataset" )  , 
                sampleInfo( "/store/user/awhitbe1/Run2015B-PromptReco_July17/Run2015B-PromptReco-v1.DoubleMuon*" , "DoubleMuon" , 1 , 1. , 1. , "Double-#mu dataset" )  ,
                sampleInfo( "/store/user/awhitbe1/Run2015B-PromptReco_July17/Run2015B-PromptReco-v1.DoubleEG*" , "DoubleElectron" , 1 , 1. , 1. , "Doube-e dataset" )  ]

samples = [ sampleInfo( "/store/user/bmahakud/PhotonTriggerStudy19thJuly2015/Spring15.GJets_HT-400To600*"                    ,  "Gjets400"        , kRed+2     , 62.05  , 0.0136   , "#gamma+jets" ) , 
            sampleInfo( "/store/user/bmahakud/PhotonTriggerStudy19thJuly2015/Spring15.GJets_HT-600ToInf*"                    ,  "Gjets600"        , kRed+2     , 20.87  , 0.00481  , "#gamma+jets" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.ZJetsToNuNu_HT-400to600*"                                         ,  "Zinv400"         , kRed+2     , 15.23  , 0.00285  , "Z(#nu#nu)+jets" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.ZJetsToNuNu_HT-600toInf*"                                         ,  "Zinv600"         , kRed+2     , 5.22   , 0.000954 , "Z(#nu#nu)+jets" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.DYJetsToLL_M-50_HT-400to600*"                                     ,  "DYJets400"       , kOrange+1     , 6.546  , 0.00133  , "Drell-Yan+jets" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.DYJetsToLL_M-50_HT-600toInf*"                                     ,  "DYJets600"       , kOrange+1     , 2.179  , 0.000490 , "Drell-Yan+jets" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.QCD_HT-500To1000_13TeV-madgraph_ext1_[0-9]_RA2AnalysisTree.root"  ,  "QCD500ext1"      , kGreen+2   , 26740. , 57.66    , "QCD" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.QCD_HT_1000ToInf_13TeV-madgraph_ext1_[0-9]_RA2AnalysisTree.root"  ,  "QCD1000ext1"     , kGreen+2   , 769.7  , 3.33     , "QCD" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.QCD_HT-500To1000_13TeV-madgraph_[0-9]_RA2AnalysisTree.root"       ,  "QCD500"          , kGreen+2   , 26740. , 458.50   , "QCD" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.QCD_HT_1000ToInf_13TeV-madgraph_[0-9]_RA2AnalysisTree.root"       ,  "QCD1000"         , kGreen+2   , 769.7  , 1.65     , "QCD" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.TTJets_MSDecaysCKM*"                                              ,  "TTJets"          , kCyan      , 806.1  , 0.0342   , "t#bar{t}" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.WJetsToLNu_HT-400to600*"                                          ,  "WJets400"        , kOrange-3  , 68.40  , 0.0122   , "W+jets" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.WJetsToLNu_HT-600toInf*"                                          ,  "WJets600"        , kOrange-3  , 23.14  , 0.00422  , "W+jets" ) ,
                                                                                                                                                                                                  
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.SMS-T1bbbb_2J_mGl-1000_mLSP-900*"                                 ,  "T1bbbb_1000-900" , kMagenta+1 , 1.0    , 1.0      , "T1bbbb"        ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.SMS-T1bbbb_2J_mGl-1500_mLSP-100*"                                 ,  "T1bbbb_1500-100" , kMagenta+1 , 1.0    , 1.0      , "T1bbbb (Comp)" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.SMS-T1qqqq_2J_mGl-1000_mLSP-800*"                                 ,  "T1qqqq_1000-800" , kMagenta+1 , 1.0    , 1.0      , "T1qqqq"        ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.SMS-T1qqqq_2J_mGl-1400_mLSP-100*"                                 ,  "T1qqqq_1500-100" , kMagenta+1 , 1.0    , 1.0      , "T1qqqq (Comp)" ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.SMS-T1tttt_2J_mGl-1200_mLSP-800*"                                 ,  "T1tttt_1200-800" , kMagenta+1 , 1.0    , 1.0      , "T1tttt"        ) ,
            sampleInfo( "/store/user/awhitbe1/PHYS14productionV15/PHYS14.SMS-T1tttt_2J_mGl-1500_mLSP-100*"                                 ,  "T1tttt_1500-100" , kMagenta+1 , 1.0    , 1.0      , "T1tttt (Comp)" )
            ]

# --------------------------------
# some utilities for loading and |
# looping over kevin's trees     |
# --------------------------------
baseDirPedro = "/eos/uscms/store/user/pedrok/SUSY2015/Analysis/dphitest/tree_GJet_CleanVars/"

samplesPedro = [ sampleInfo(    "tree_WJetsToLNu_HT-400to600.root"       , "WJetsToLNu_HT-400to600"  , kOrange-3 , 68.40 ),
                 sampleInfo(    "tree_WJetsToLNu_HT-600toInf_part1.root" , "WJetsToLNu_HT-600toInf_part1" , kOrange-3 , 23.14 ),
                 sampleInfo(    "tree_WJetsToLNu_HT-600toInf_part2.root" , "WJetsToLNu_HT-600toInf_part2" , kOrange-3 , 23.14 ),
                 sampleInfo("tree_WJetsToLNu_HT-600toInf_part3.root" , "WJetsToLNu_HT-600toInf_part3"     , kOrange-3 , 23.14 ),
                 sampleInfo("tree_QCD_HT-500to1000.root"      , "QCD_HT-500to1000"      , kGreen+2 , 26740 ),
                 sampleInfo("tree_QCD_HT-500to1000_ext1.root" , "QCD_HT-500to1000_ext1" , kGreen+2 , 26740 ),
                 sampleInfo("tree_QCD_HT-1000toInf.root"      , "QCD_HT-1000toInf"      , kGreen+2 , 769.7 ),
                 sampleInfo("tree_QCD_HT-1000toInf_ext1.root" , "QCD_HT-1000toInf_ext1" , kGreen+2 , 769.7 ), 
                 sampleInfo("tree_TTJets_part1.root" , "TTJets_part1" , kCyan , 806.1 ),
                 sampleInfo("tree_TTJets_part2.root" , "TTJets_part2" , kCyan , 806.1 ),
                 sampleInfo("tree_TTJets_part3.root" , "TTJets_part3" , kCyan , 806.1 ),
                 sampleInfo("tree_TTJets_part4.root" , "TTJets_part4" , kCyan , 806.1 ),
                 sampleInfo("tree_TTJets_part5.root" , "TTJets_part5" , kCyan , 806.1 ),
                 sampleInfo(    "tree_GJets_HT-400to600.root"  , "GJets_HT-400to600" , kRed+2 , 62.05 ) ,
                 sampleInfo(    "tree_GJets_HT-600toInf.root"  , "GJets_HT-600toInf" , kRed+2 , 20.87 ) 
                 ]
    

