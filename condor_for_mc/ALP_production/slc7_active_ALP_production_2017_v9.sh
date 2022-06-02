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

random_number=`expr $RANDOM / 100 + 1`
echo "sleep ${random_number} s to avoid singularity conflict"
sleep ${random_number}

# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
filename="ROOTNAME_$2_$3.root"
echo ${filename}

cat WRAPPER.sh | bash cmssw-cc7.sh

echo ${filename}
cp SMP-RunIISummer20UL17NanoAODv9-00081.root /eos/user/s/sdeng/WZG_analysis/ALP/fa_200G/2017/ROOTNAME/${filename}