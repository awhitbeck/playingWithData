from os import system

skeleton = """universe = vanilla
Executable = jobExecCondor_NminusOnePhoton.sh
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" )
request_disk = 1000000
request_memory = 199
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = jobExecCondor_NminusOnePhoton.sh,inputFiles.py,commissioningUtils.py,plotNminusOnePhoton_batch.py,photonUtils.py,RA2Utils.py,triggerUtils.py
Output = NminusOnePhoton_{0}_$(Cluster).stdout
Error = NminusOnePhoton_{0}_$(Cluster).stderr
Log = NminusOnePhoton_{0}_$(Cluster).condor
notification = Error
notify_user = awhitbe1@FNAL.GOV
x509userproxy = $ENV(X509_USER_PROXY)
Arguments = {0}
Queue 1"""

samples = [ "Gjets400" , "Gjets600" , 

            "DYJets400" , "DYJets600" , 

            "QCDpt80" , "QCDpt120" , "QCDpt170" , "QCDpt300" , 
            "QCDpt470" , "QCDpt600" , "QCDpt800" , "QCDpt1000" ,
            "QCDpt1400" , "QCDpt1800" , "QCDpt2400" , "QCDpt3200" , 

            "TTJets" ,

            "WJets400" , "WJets600" , 

            "SinglePhoton"
            ]

for s in samples :

    file = open("NminusOnePhoton_{0}.jdl".format(s),"w")
    file.write(skeleton.format(s))
    file.close()

    system("condor_submit NminusOnePhoton_{0}.jdl".format(s))
    
