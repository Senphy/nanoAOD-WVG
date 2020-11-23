
# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export Proxy_path=/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738
voms-proxy-info -all
voms-proxy-info -all -file $Proxy_path


# lhe level production
export SCRAM_ARCH=slc6_amd64_gcc481
scramv1 project CMSSW CMSSW_7_1_20
cd CMSSW_7_1_20/src
eval `scramv1 runtime -sh`
curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIIWinter15wmLHE-00070 --retry 2 --create-dirs -o Configuration/GenProduction/python/SMP-RunIIWinter15wmLHE-00070-fragment.py
sed -i -e 's/\/cvmfs\/cms.cern.ch\/phys_generator\/gridpacks\/slc6_amd64_gcc481\/13TeV\/madgraph\/V5_2.3.2.2\/WVAToLNu2JA_4f_NLO\/v1\/WZAToLNu2jA_4f_NLO_tarball.tar.xz/..\/WZG_scheme3_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz/g' \
    Configuration/GenProduction/python/SMP-RunIIWinter15wmLHE-00070-fragment.py 
cp ../../randomizeSeeds.py Configuration/GenProduction/python/
scram b
cd ../../
cmsDriver.py Configuration/GenProduction/python/SMP-RunIIWinter15wmLHE-00070-fragment.py  \
    --fileout file:SMP-RunIIWinter15wmLHE-00070.root \
    --mc \
    --eventcontent LHE \
    --datatier LHE \
    --conditions MCRUN2_71_V1::All \
    --step LHE \
    --python_filename SMP-RunIIWinter15wmLHE-00070_1_cfg.py \
    --no_exec \
    --customise Configuration/DataProcessing/Utils.addMonitoring,Configuration/GenProduction/randomizeSeeds.randomizeSeeds -n 1000 || exit $? ;

cmsRun SMP-RunIIWinter15wmLHE-00070_1_cfg.py

# GS level
scramv1 project CMSSW CMSSW_7_1_20_patch3
cd CMSSW_7_1_20_patch3/src
eval `scramv1 runtime -sh`
curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIISummer15GS-00062 --retry 2 --create-dirs -o Configuration/GenProduction/python/SMP-RunIISummer15GS-00062-fragment.py
scram b
cd ../../
cmsDriver.py Configuration/GenProduction/python/SMP-RunIISummer15GS-00062-fragment.py \
    --filein file:SMP-RunIIWinter15wmLHE-00070.root  \
    --fileout file:SMP-RunIISummer15GS-00062.root \
    --mc \
    --eventcontent RAWSIM,DQM \
    --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring \
    --datatier GEN-SIM,DQMIO \
    --conditions MCRUN2_71_V1::All \
    --beamspot Realistic50ns13TeVCollision \
    --step GEN,SIM,VALIDATION:genvalid_all \
    --magField 38T_PostLS1 \
    --python_filename SMP-RunIISummer15GS-00062_1_cfg.py \
    --no_exec -n 1000 || exit $? ;

cmsRun SMP-RunIISummer15GS-00062_1_cfg.py


# pileup level
export SCRAM_ARCH=slc6_amd64_gcc530
scramv1 project CMSSW CMSSW_8_0_21
cd CMSSW_8_0_21/src
eval `scramv1 runtime -sh`
scram b
cd ../../
cmsDriver.py step1 \
    --filein file:SMP-RunIISummer15GS-00062.root \
    --fileout file:SMP-RunIISummer16DR80Premix-00005_step1.root  \
    --pileup_input "filelist:pileup_filelist_16.txt" \
    --mc \
    --eventcontent PREMIXRAW \
    --datatier GEN-SIM-RAW \
    --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 \
    --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 \
    --nThreads 4 \
    --datamix PreMix \
    --era Run2_2016 \
    --python_filename SMP-RunIISummer16DR80Premix-00005_1_cfg.py \
    --no_exec \
    --customise Configuration/DataProcessing/Utils.addMonitoring -n 1000 || exit $? ;
cmsRun SMP-RunIISummer16DR80Premix-00005_1_cfg.py

cmsDriver.py step2 \
    --filein file:SMP-RunIISummer16DR80Premix-00005_step1.root \
    --fileout file:SMP-RunIISummer16DR80Premix-00005.root \
    --mc \
    --eventcontent AODSIM \
    --runUnscheduled \
    --datatier AODSIM \
    --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 \
    --step RAW2DIGI,RECO,EI \
    --nThreads 4 \
    --era Run2_2016 \
    --python_filename SMP-RunIISummer16DR80Premix-00005_2_cfg.py \
    --no_exec \
    --customise Configuration/DataProcessing/Utils.addMonitoring -n 1000 || exit $? ;
cmsRun SMP-RunIISummer16DR80Premix-00005_2_cfg.py


# MiniAODSIM level
export SCRAM_ARCH=slc6_amd64_gcc630
scramv1 project CMSSW CMSSW_9_4_9
cd CMSSW_9_4_9/src
eval `scramv1 runtime -sh`
scram b
cd ../../
cmsDriver.py step1 \
    --filein file:SMP-RunIISummer16DR80Premix-00005.root \
    --fileout file:SMP-RunIISummer16MiniAODv3-00212.root \
    --mc \
    --eventcontent MINIAODSIM \
    --runUnscheduled \
    --datatier MINIAODSIM \
    --conditions 94X_mcRun2_asymptotic_v3 \
    --step PAT \
    --nThreads 8 \
    --era Run2_2016,run2_miniAOD_80XLegacy \
    --python_filename SMP-RunIISummer16MiniAODv3-00212_1_cfg.py \
    --no_exec \
    --customise Configuration/DataProcessing/Utils.addMonitoring -n 1000 || exit $? ;
cmsRun SMP-RunIISummer16MiniAODv3-00212_1_cfg.py


# NanoAODSIM level
export SCRAM_ARCH=slc6_amd64_gcc700
scramv1 project CMSSW CMSSW_10_2_18
cd CMSSW_10_2_18/src
eval `scramv1 runtime -sh`
scram b
cd ../../
cmsDriver.py step1 \
    --filein file:SMP-RunIISummer16MiniAODv3-00212.root \
    --fileout file:SMP-RunIISummer16NanoAODv6-00310.root \
    --mc \
    --eventcontent NANOEDMAODSIM \
    --datatier NANOAODSIM \
    --conditions 102X_mcRun2_asymptotic_v7 \
    --step NANO \
    --nThreads 2 \
    --era Run2_2016,run2_nanoAOD_94X2016 \
    --python_filename SMP-RunIISummer16NanoAODv6-00310_1_cfg.py \
    --no_exec \
    --customise Configuration/DataProcessing/Utils.addMonitoring -n 1000 || exit $? ;

sed -i -e 's/PoolOutputModule/NanoAODOutputModule/g' SMP-RunIISummer16NanoAODv6-00310_1_cfg.py
cmsRun SMP-RunIISummer16NanoAODv6-00310_1_cfg.py

# exit singularity
exit
