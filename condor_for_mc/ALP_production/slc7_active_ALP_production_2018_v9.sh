#!/usr/bin/env bash
# exit_on_error() {
#     result=$1
#     code=$2
#     message=$3

#     if [ $1 != 0 ]; then
#         echo $3
#         exit $2
#     fi
# }
echo $1 $2 $3

# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
filename="ROOTNAME_$2_$3.root"
echo ${filename}

cat WRAPPER.sh | bash cmssw-cc7.sh

echo ${filename}
cp SMP-RunIISummer20UL18NanoAODv9-00091.root /eos/user/s/sdeng/WZG_analysis/ALP/2018/ROOTNAME/${filename}