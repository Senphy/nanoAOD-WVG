#!/usr/bin/env bash
start=`date +%s`
# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
Proxy_path='/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738'
export X509_USER_PROXY=${Proxy_path}
export SCRAM_ARCH=slc7_amd64_gcc700
voms-proxy-info -all
voms-proxy-info -all -file ${Proxy_path} -valid 192:0
EVENTS=100


# lhe-gen level production
if [ -r CMSSW_10_6_22/src ] ; then
  echo release CMSSW_10_6_22 already exists
else
  scram p CMSSW CMSSW_10_6_22
fi
cd CMSSW_10_6_22/src
eval `scram runtime -sh`

curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIISummer20UL17wmLHEGEN-00238 --retry 3 --create-dirs -o Configuration/GenProduction/python/SMP-RunIISummer20UL17wmLHEGEN-00238-fragment.py
[ -s Configuration/GenProduction/python/SMP-RunIISummer20UL17wmLHEGEN-00238-fragment.py ] || exit $?;
sed -i -e 's/\/cvmfs\/cms.cern.ch\/phys_generator\/gridpacks\/slc7_amd64_gcc700\/13TeV\/madgraph\/V5_2.6.5\/WZAToLNuLLA_4f_NLO\/WZAToLNuLLA_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/..\/TARBALLNAME/g' \
    Configuration/GenProduction/python/SMP-RunIISummer20UL17wmLHEGEN-00238-fragment.py
cp ../../randomizeSeeds.py Configuration/GenProduction/python/
scram b
cd ../..
cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer20UL17wmLHEGEN-00238-fragment.py \
        --python_filename SMP-RunIISummer20UL17wmLHEGEN-00238_1_cfg.py \
        --eventcontent RAWSIM,LHE \
        --customise Configuration/DataProcessing/Utils.addMonitoring,Configuration/GenProduction/randomizeSeeds.randomizeSeeds \
        --datatier GEN,LHE \
        --fileout file:SMP-RunIISummer20UL17wmLHEGEN-00238.root \
        --conditions 106X_mc2017_realistic_v6 \
        --beamspot Realistic25ns13TeVEarly2017Collision \
        --step LHE,GEN \
        --geometry DB:Extended \
        --era Run2_2017 \
        --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL17wmLHEGEN-00238_1_cfg.py

# SIM level
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17SIM-00084_1_cfg.py \
            --eventcontent RAWSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM \
            --fileout file:SMP-RunIISummer20UL17SIM-00084.root \
            --conditions 106X_mc2017_realistic_v6 \
            --beamspot Realistic25ns13TeVEarly2017Collision \
            --step SIM \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL17wmLHEGEN-00238.root \
            --era Run2_2017 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL17SIM-00084_1_cfg.py

# DIGI level
cmsDriver.py  --python_filename SMP-RunIISummer20UL17DIGIPremix-00084_1_cfg.py \
            --eventcontent PREMIXRAW \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM-DIGI \
            --fileout file:SMP-RunIISummer20UL17DIGIPremix-00084.root \
            --pileup_input "filelist:filepath_Neutrino_E-10_gun_2017.txt" \
            --conditions 106X_mc2017_realistic_v6 \
            --step DIGI,DATAMIX,L1,DIGI2RAW \
            --procModifiers premix_stage2 \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL17SIM-00084.root \
            --datamix PreMix \
            --era Run2_2017 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL17DIGIPremix-00084_1_cfg.py

# HLT level
if [ -r CMSSW_9_4_14_UL_patch1/src ] ; then
  echo release CMSSW_9_4_14_UL_patch1 already exists
else
  scram p CMSSW CMSSW_9_4_14_UL_patch1
fi
cd CMSSW_9_4_14_UL_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17HLT-00084_1_cfg.py \
            --eventcontent RAWSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier GEN-SIM-RAW \
            --fileout file:SMP-RunIISummer20UL17HLT-00084.root \
            --conditions 94X_mc2017_realistic_v15 \
            --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
            --step HLT:2e34v40 \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL17DIGIPremix-00084.root \
            --era Run2_2017 \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL17HLT-00084_1_cfg.py

# RECO level
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17RECO-00084_1_cfg.py \
            --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier AODSIM \
            --fileout file:SMP-RunIISummer20UL17RECO-00084.root \
            --conditions 106X_mc2017_realistic_v6 \
            --step RAW2DIGI,L1Reco,RECO,RECOSIM \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL17HLT-00084.root \
            --era Run2_2017 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL17RECO-00084_1_cfg.py

# MINIAODSIM LEVEL
if [ -r CMSSW_10_6_20/src ] ; then
  echo release CMSSW_10_6_20 already exists
else
  scram p CMSSW CMSSW_10_6_20
fi
cd CMSSW_10_6_20/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17MiniAODv2-00082_1_cfg.py \
            --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier MINIAODSIM \
            --fileout file:SMP-RunIISummer20UL17MiniAODv2-00082.root \
            --conditions 106X_mc2017_realistic_v9 \
            --step PAT \
            --procModifiers run2_miniAOD_UL \
            --geometry DB:Extended \
            --filein file:SMP-RunIISummer20UL17RECO-00084.root \
            --era Run2_2017 \
            --runUnscheduled \
            --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SMP-RunIISummer20UL17MiniAODv2-00082_1_cfg.py

# Nano LEVEL
if [ -r CMSSW_10_6_26/src ] ; then
  echo release CMSSW_10_6_26 already exists
else
  scram p CMSSW CMSSW_10_6_26
fi
cd CMSSW_10_6_26/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SMP-RunIISummer20UL17NanoAODv9-00081_1_cfg.py \
            --eventcontent NANOEDMAODSIM \
            --customise Configuration/DataProcessing/Utils.addMonitoring \
            --datatier NANOAODSIM \
            --fileout file:SMP-RunIISummer20UL17NanoAODv9-00081.root \
            --conditions 106X_mc2017_realistic_v9 \
            --step NANO \
            --filein file:SMP-RunIISummer20UL17MiniAODv2-00082.root \
            --era Run2_2017,run2_nanoAOD_106Xv2 \
            --no_exec --mc -n $EVENTS || exit $? ;

sed -i -e 's/PoolOutputModule/NanoAODOutputModule/g' SMP-RunIISummer20UL17NanoAODv9-00081_1_cfg.py
cmsRun SMP-RunIISummer20UL17NanoAODv9-00081_1_cfg.py


end=`date +%s`
time=`echo $start $end | awk '{print $2-$1}'`
echo $time
