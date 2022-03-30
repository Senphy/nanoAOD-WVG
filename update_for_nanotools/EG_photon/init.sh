#!/bin/bash
export WORKING_PATH="$CMSSW_BASE/src/PhysicsTools/NanoAODTools/"
export prev_path=$PWD
echo "Current path: $prev_path"

echo "Update for photon SF"
cp -r $WORKING_PATH/nanoAOD-WVG/update_for_nanotools/EG_photon/ $WORKING_PATH/data/

unset WORKING_PATH
echo "Initing Done \(ᵔᵕᵔ)/"
