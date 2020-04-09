#!/usr/bin/env bash
exit_on_error() {
    result=$1
    code=$2
    message=$3

    if [ $1 != 0 ]; then
        echo $3
        exit $2
    fi
}

#### FRAMEWORK SANDBOX SETUP ####
# Load cmssw_setup function
source cmssw_setup.sh

# Setup CMSSW Base
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# Download sandbox, replace it when you have different sandbox_name
sandbox_name="sandbox-CMSSW_7_1_20_patch3-6036b93.tar.bz2"
# Change to your own http
xrdcp -s root://eosuser.cern.ch///eos/user/s/sdeng/public/$sandbox_name .

# Setup framework from sandbox
cmssw_setup $sandbox_name || exit_on_error $? 151 "Could not unpack sandbox"
#### END OF FRAMEWORK SANDBOX SETUP ####

# Enter script directory
cd $CMSSW_BASE/src/test
date
# pythia run
cmsRun SMP-RunIISummer15GS-00062_1_cfg.py

date
# Clean up
cd -
# Move the file you need to the initial path
DATE=`date +%F | sed 's/-/_/g'`
mkdir -p /eos/user/s/sdeng/WZG_analysis/$DATE
cp $CMSSW_BASE/src/test/SMP-RunIISummer15GS-00062.root /eos/user/s/sdeng/WZG_analysis/$DATE 
cp $CMSSW_BASE/src/test/SMP-RunIISummer15GS-00062.root .
rm $sandbox_name