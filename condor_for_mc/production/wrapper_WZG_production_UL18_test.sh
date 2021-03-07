#!/usr/bin/env bash

# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
EVENTS=1000

# lhe-gen level production
export SCRAM_ARCH=slc7_amd64_gcc700
scramv1 project CMSSW CMSSW_10_6_19_patch3 
cd CMSSW_10_6_19_patch3/src
eval `scramv1 runtime -sh`
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SUS-RunIISummer20UL18wmLHEGEN-00040 --retry 3 --create-dirs -o Configuration/GenProduction/python/SUS-RunIISummer20UL18wmLHEGEN-00040-fragment.py
sed -i -e 's/\/cvmfs\/cms.cern.ch\/phys_generator\/gridpacks\/UL\/13TeV\/madgraph\/V5_2.6.5\/WZGToLNu2jG_4f_NLO\/WZGToLNu2jG_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/..\/WZAToLNuLLA_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/g' \
    Configuration/GenProduction/python/SUS-RunIISummer20UL18wmLHEGEN-00040-fragment.py 
cp ../../randomizeSeeds.py Configuration/GenProduction/python/
scram b
cd ../../
cmsDriver.py Configuration/GenProduction/python/SUS-RunIISummer20UL18wmLHEGEN-00040-fragment.py  \
    --python_filename SUS-RunIISummer20UL18wmLHEGEN-00040_1_cfg.py \
    --eventcontent RAWSIM,LHE   \
    --customise Configuration/DataProcessing/Utils.addMonitoring,Configuration/GenProduction/randomizeSeeds.randomizeSeeds \
    --datatier GEN,LHE \
    --fileout file:SUS-RunIISummer20UL18wmLHEGEN-00040.root \
    --conditions 106X_upgrade2018_realistic_v4 \
    --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" \
    --beamspot Realistic25ns13TeVEarly2018Collision \
    --step LHE,GEN \
    --geometry DB:Extended \
    --era Run2_2018 \
    --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SUS-RunIISummer20UL18wmLHEGEN-00040_1_cfg.py

# SIM level
scramv1 project CMSSW CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
eval `scramv1 runtime -sh`
scram b
cd ../../
cmsDriver.py    --python_filename SUS-RunIISummer20UL18SIM-00009_1_cfg.py \
    --eventcontent RAWSIM \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM \
    --fileout file:SUS-RunIISummer20UL18SIM-00009.root \
    --conditions 106X_upgrade2018_realistic_v11_L1v1 \
    --beamspot Realistic25ns13TeVEarly2018Collision \
    --step SIM \
    --geometry DB:Extended \
    --filein file:SUS-RunIISummer20UL18wmLHEGEN-00040.root \
    --era Run2_2018 \
    --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;
    
cmsRun SUS-RunIISummer20UL18SIM-00009_1_cfg.py


# DIGI level
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scramv1 runtime -sh`
scram b
cd ../../
cmsDriver.py --python_filename SUS-RunIISummer20UL18DIGIPremix-00009_1_cfg.py \
    --eventcontent PREMIXRAW \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM-DIGI \
    --fileout file:SUS-RunIISummer20UL18DIGIPremix-00009.root \
    --pileup_input "filelist:filepath_Neutrino_E-10_gun.txt" \
    --conditions 106X_upgrade2018_realistic_v11_L1v1 \
    --step DIGI,DATAMIX,L1,DIGI2RAW \
    --procModifiers premix_stage2 \
    --geometry DB:Extended \
    --filein file:SUS-RunIISummer20UL18SIM-00009.root \
    --datamix PreMix \
    --era Run2_2018 \
    --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SUS-RunIISummer20UL18DIGIPremix-00009_1_cfg.py


# HLT level
if [ -r CMSSW_10_2_16_UL/src ] ; then
  echo release CMSSW_10_2_16_UL already exists
else
  scram p CMSSW CMSSW_10_2_16_UL
fi
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`
scram b
cd ../../
cmsDriver.py --python_filename SUS-RunIISummer20UL18HLT-00009_1_cfg.py \
    --eventcontent RAWSIM \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM-RAW \
    --fileout file:SUS-RunIISummer20UL18HLT-00009.root \
    --conditions 102X_upgrade2018_realistic_v15 \
    --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' \
    --step HLT:2018v32 \
    --geometry DB:Extended \
    --filein file:SUS-RunIISummer20UL18DIGIPremix-00009.root \
    --era Run2_2018 \
    --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SUS-RunIISummer20UL18HLT-00009_1_cfg.py


# RECO level
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scramv1 runtime -sh`
scram b
cd ../../
cmsDriver.py --python_filename SUS-RunIISummer20UL18RECO-00009_1_cfg.py \
    --eventcontent AODSIM \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier AODSIM \
    --fileout file:SUS-RunIISummer20UL18RECO-00009.root \
    --conditions 106X_upgrade2018_realistic_v11_L1v1 \
    --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI \
    --geometry DB:Extended \
    --filein file:SUS-RunIISummer20UL18HLT-00009.root \
    --era Run2_2018 \
    --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;

cmsRun SUS-RunIISummer20UL18RECO-00009_1_cfg.py


# MINIAODSIM LEVEL
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename SUS-RunIISummer20UL18MiniAOD-00009_1_cfg.py \
    --eventcontent MINIAODSIM \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier MINIAODSIM \
    --fileout file:SUS-RunIISummer20UL18MiniAOD-00009.root \
    --conditions 106X_upgrade2018_realistic_v11_L1v1 \
    --step PAT \
    --geometry DB:Extended \
    --filein file:SUS-RunIISummer20UL18RECO-00009.root \
    --era Run2_2018 \
    --runUnscheduled --no_exec --mc -n $EVENTS || exit $? 

cmsRun SUS-RunIISummer20UL18MiniAOD-00009_1_cfg.py


# Nano LEVEL
if [ -r CMSSW_10_6_19_patch2/src ] ; then
  echo release CMSSW_10_6_19_patch2 already exists
else
  scram p CMSSW CMSSW_10_6_19_patch2
fi
cd CMSSW_10_6_19_patch2/src
eval `scram runtime -sh`
scram b
cd ../..
cmsDriver.py  --python_filename WZG_UL18_Nano_cfg.py \
    --eventcontent NANOEDMAODSIM \
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --datatier NANOAODSIM \
    --fileout file:WZG_UL18_Nano.root \
    --conditions 106X_upgrade2018_realistic_v15_L1v1 \
    --step NANO \
    --filein file:SUS-RunIISummer20UL18MiniAOD-00009.root \
    --era Run2_2018,run2_nanoAOD_106Xv1 \
    --no_exec --mc -n $EVENTS || exit $? ;

sed -i -e 's/PoolOutputModule/NanoAODOutputModule/g' WZG_UL18_Nano_cfg.py
cmsRun WZG_UL18_Nano_cfg.py


