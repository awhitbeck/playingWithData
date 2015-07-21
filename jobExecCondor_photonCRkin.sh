#!/bin/sh

SAMPLE=$1

echo "SAMPLE: "$SAMPLE
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /uscms_data/d2/awhitbe1/workArea/RA2studies/commission2015/CMSSW_7_4_6_patch6/src/
eval `scramv1 runtime -sh`
cd -

python plotPhotonCRkinematics_batch.py -s $SAMPLE