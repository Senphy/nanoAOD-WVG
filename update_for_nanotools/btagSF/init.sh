#!/bin/bash
export WORKING_PATH="$CMSSW_BASE/src/PhysicsTools/NanoAODTools/"
export prev_path=$PWD
echo "Current path: $prev_path"

echo "Update for btv"
echo "Updating btag SF"
cp $WORKING_PATH/nanoAOD-WVG/update_for_nanotools/btagSF/*DeepCSV*.csv $WORKING_PATH/data/btagSF/
echo "Updating btagSF module"
cp $WORKING_PATH/nanoAOD-WVG/update_for_nanotools/btagSF/btagSFProducer.py $WORKING_PATH/python/postprocessing/modules/btv/

echo -e "\nRecompiling..."
cd $CMSSW_BASE/src
scram b -j4
cd $prev_path
unset prev_path
echo -e "Compiling complete\n"

unset WORKING_PATH
echo "Initing Done \(ᵔᵕᵔ)/"
