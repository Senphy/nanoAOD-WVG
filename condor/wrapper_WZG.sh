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
sandbox_name1="sandbox-CMSSW_7_1_20-4dd66ac.tar.bz2"
sandbox_name2="sandbox-CMSSW_7_1_20_patch3-9e5cf1d.tar.bz2"
sandbox_name3="sandbox-CMSSW_8_0_21-df507c8.tar.bz2"
sandbox_name4="sandbox-CMSSW_9_4_9-24e4b50.tar.bz2"
sandbox_name5="sandbox-CMSSW_10_2_18-fb0abee.tar.bz2"

cfg_name1="SMP-RunIIWinter15wmLHE-00070_1_cfg.py"
cfg_name2="SMP-RunIISummer15GS-00062_1_cfg.py"
cfg_name31="SMP-RunIISummer16DR80Premix-00005_1_cfg.py"
cfg_name32="SMP-RunIISummer16DR80Premix-00005_2_cfg.py"
cfg_name4="SMP-RunIISummer16MiniAODv3-00212_1_cfg.py"
cfg_name5="SMP-RunIISummer16NanoAODv6-00310_1_cfg.py"

root_name1="SMP-RunIIWinter15wmLHE-00070.root"
root_name2="SMP-RunIISummer15GS-00062.root"
root_name3="SMP-RunIISummer16DR80Premix-00005.root"
root_name4="SMP-RunIISummer16MiniAODv3-00212.root"
root_name5="SMP-RunIISummer16NanoAODv6-00310.root"
# Change to your own http
#xrdcp -s root://eosuser.cern.ch///eos/user/s/sdeng/WZG_analysis/$sandbox_name .

# Setup framework from sandbox
cmssw_setup $sandbox_name1 || exit_on_error $? 151 "Could not unpack sandbox"
# Enter script directory
cd $CMSSW_BASE/src/submit
cmsRun $cfg_name1 
# Clean up
cd -
cp $CMSSW_BASE/src/submit/$root_name1 .
rm $sandbox_name1
rm -rf cmssw-tmp

# GS
cmssw_setup $sandbox_name2
mv $root_name1 $CMSSW_BASE/src/submit/
cd $CMSSW_BASE/src/submit
cmsRun $cfg_name2 
cd -
cp $CMSSW_BASE/src/submit/$root_name2 .
rm $sandbox_name2
rm -rf cmssw-tmp

# DR
cmssw_setup $sandbox_name3
mv $root_name2 $CMSSW_BASE/src/submit/
cd $CMSSW_BASE/src/submit
cmsRun $cfg_name31
cmsRun $cfg_name32 
cd -
cp $CMSSW_BASE/src/submit/$root_name3 .
rm $sandbox_name3
rm -rf cmssw-tmp

# MiniAOD
cmssw_setup $sandbox_name4
mv $root_name3 $CMSSW_BASE/src/submit/
cd $CMSSW_BASE/src/submit
cmsRun $cfg_name4 
cd -
cp $CMSSW_BASE/src/submit/$root_name4 .
rm $sandbox_name4
rm -rf cmssw-tmp

# NanoAOD
cmssw_setup $sandbox_name5
mv $root_name4 $CMSSW_BASE/src/submit/
cd $CMSSW_BASE/src/submit
cmsRun $cfg_name5 
cd -
cp $CMSSW_BASE/src/submit/$root_name5 .
rm $sandbox_name5
rm -rf cmssw-tmp
