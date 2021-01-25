#! /bin/bash

# Wrapper to setup the CMSSW framework 
# from a sandbox

cmssw_setup() {
    ####################################
    #Setup CMSSW framework
    # Usage: setup_cmssw sandbox.tar.bz2
    ###################################
    #Download and extract sandbox
    tar xjf "$1"
    
    #Keep track of release sandbox version 
    basedir=$PWD
    rel=$(dirname $(tar -tvjf "$1" | head -1 | awk '{print $NF}'))
    #rel=$(echo CMSSW_*)
    arch=$(ls $rel/.SCRAM/|grep slc)
    old_release_top=$(awk -F= '/RELEASETOP/ {print $2}' $rel/.SCRAM/slc*/Environment)
    tmp=$basedir/$rel
    
    # Creating new release
    # This is done so e.g CMSSW_BASE and other variables are not hardcoded to the sandbox setting paths
    # which will not exist here
    echo ">>> creating new release $rel"
    mkdir cmssw-tmp
    cd cmssw-tmp
    scramv1 project -f CMSSW $rel
    new_release_top=$(awk -F= '/RELEASETOP/ {print $2}' $rel/.SCRAM/slc*/Environment)
    cd $rel
    echo ">>> preparing sandbox release $rel"
    for i in bin lib python src; do
        rm -rf "$i"
        mv "$basedir/$rel/$i" .
    done
    
    # Fixing python paths
    for f in $(find -iname __init__.py); do
        sed -i -e "s@$old_release_top@$new_release_top@" "$f"
    done
    
    # Delete old cmssw framework
    rm -rf $tmp

    eval $(scramv1 runtime -sh)
    cd "$basedir"
    
    echo "[$(date '+%F %T')] wrapper ready"
    echo "current directory: $PWD"
    # cd $CMSSW_BASE
    echo $CMSSW_BASE
}

#setup_cmssw sandbox-CMSSW_7_2_3-86c7ff0.tar.bz2
