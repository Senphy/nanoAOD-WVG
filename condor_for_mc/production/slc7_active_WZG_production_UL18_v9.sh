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

# set up cmssw
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh


cat wrapper_WZG_production_UL18_v9.sh | bash cmssw-cc7
