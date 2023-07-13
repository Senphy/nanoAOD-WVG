#!/usr/bin/env bash
# path file year skim_name isdata
echo $1 $2 $3 $4 $5

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# set up cmssw
export SCRAM_ARCH=slc7_amd64_gcc700
source cmssw_setup.sh
cmssw_setup sandbox-CMSSW_10_6_29-WZG.tar.bz2

# process
export EOS_MGM_URL=root://eosuser.cern.ch
file="${1}/${3}/${2}"
eos cp ${file} .
python Apply_weight_Template_postproc.py -f ${2} -y ${3} ${5}
output="${1}/${3}/test/${2}"
echo $output
eos cp ${4} ${output}
rm *