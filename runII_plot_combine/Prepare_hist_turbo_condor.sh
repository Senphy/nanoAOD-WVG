#!/usr/bin/env bash
# path file year skim_name isdata
echo $1 $2 $3 $4 $5 $6 $7 $8
path=$1
filename=$2
year=$3
type=$4
region=$5
output_filename=$6

for i in "$@"
do
    case $i in
        isdata=*)
        isdata="${i#*=}"
        ;;
    esac
    case $i in
        mcname=*)
        mcname="${i#*=}"
        ;;
    esac
done

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh

# set up anaconda
export SCRAM_ARCH=slc7_amd64_gcc700
source /afs/cern.ch/user/s/sdeng/conda_set.sh
conda activate jupyter_host

# process
export EOS_MGM_URL=root://eosuser.cern.ch
eos cp ${path}/${filename} .
if [ -z $isdata ]; then
    python3 Prepare_hist_turbo_condor.py -m prepare -f ${filename} -y ${year} -r ${region} -t ${type} -n ${mcname}
else
    python3 Prepare_hist_turbo_condor.py -m prepare -f ${filename} -y ${year} -r ${region} -t ${type} ${isdata}
fi
output="/eos/user/s/sdeng/WZG_analysis/hists/"
echo $output

if [ -e $output_filename ]; then
    eos cp $output_filename ${output}
else
    touch fail_$output_filename 
    eos cp fail_$output_filename ${output}
fi
rm *.root