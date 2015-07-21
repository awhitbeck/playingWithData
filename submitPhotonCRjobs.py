from os import system

skeleton = """universe = vanilla
Executable = jobExecCondor_photonCRkin.sh
Requirements = OpSys == "LINUX" && (Arch != "DUMMY" )
request_disk = 1000000
request_memory = 199
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = jobExecCondor_photonCRkin.sh,inputFiles.py,commissioningUtils.py,plotPhotonCRkinematics_batch.py,photonUtils.py,RA2Utils.py,triggerUtils.py
Output = photonCRkin_{0}_$(Cluster).stdout
Error = photonCRkin_{0}_$(Cluster).stderr
Log = photonCRkin_{0}_$(Cluster).condor
notification = Error
notify_user = awhitbe1@FNAL.GOV
x509userproxy = $ENV(X509_USER_PROXY)
Arguments = {0}
Queue 1"""

samples = [ "Gjets400" , "Gjets600" , "SinglePhoton" ]

for s in samples :

    file = open("jobExecCondor_photonCRkin_{0}.jdl".format(s),"w")
    file.write(skeleton.format(s))
    file.close()

    system("condor_submit jobExecCondor_photonCRkin_{0}.jdl".format(s))
    
