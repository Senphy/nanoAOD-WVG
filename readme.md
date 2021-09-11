# WZG selector
Based on NanoAOD Tools: <https://github.com/cms-nanoAOD/nanoAOD-tools>

Dedicated for WZG analysis on lxplus environment

More info are in each folder

--------------
## content

- [Download and setup](#Download-and-setup)
- [Baseline selection](#Baseline-selection)
- [Condor mode](#Condor-mode)
- [Crab mode](#Crab-mode)

--------------
<br>

## <span id="Download-and-setup"> Download and setup </span> 

```bash
cmsrel CMSSW_10_6_19
cd CMSSW_10_6_19/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools 
cd PhysicsTools/NanoAODTools
scram b
git clone https://github.com/Senphy/nanoAOD-WVG.git
cd nanoAOD-WVG
```
We need to update some files for official NanoAOD-tools. Also we need to `scram` the new modules.
```bash
mv modules/* $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/
mv update_for_nanotools/for_prefire/L1PrefiringMaps.root $CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/prefire_maps/
mv data/* $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/data/
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools
scram b
```
<br>

## <span id="Baseline-selection"> Baseline selection local test</span>
In WZG_seletor, `WZG_Module.py` is designed for basic selection (e.g. pt cut). Use `WZG_postproc.py` for local test.

```bash
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/WZG_selector
python WZG_postproc.py -h
```

arguments:
- `-f`  specify the input file. For local file e.g. `/afs/xxx.root`. For DAS file e.g. `root://xxx`. In condor mode it should be dataset name e.g. /WZG/XXX/NanoAODSIM. If an input file is not provided, assume this is a crab job.
- `-m`  Run mode. Normally use `local`. `condor` mode is designed as an interface for `condor_for_postproc.py` in condor folder.


`DAS_filesearch.py` is designed for returning LFN from given dataset. And store LFN into given filepath_GIVENFILENAME.txt. Then it will call `test_ValidSite_cfy.py` to search the valid site which can get access to the LFN.

<br>

## <span id="Condor-mode"> Condor mode </span>
Condor mode mainly is designed for MC production and postproceeing MC samples. Since the HTCondor sometimes can't get access to some sites, it is still recommended to use crab to handle MC samples. 
In condor folder, `condor_for_postproc.py` is designed for preparing codes and submitting them to HTcondor. The purpose is to run over samples on DAS in parallel. It has `-f` arguments to load input json.

First you need to setup grid certification
```bash
voms-proxy-info -voms cms -valid 192:0
```
Modify `Proxy_path` in `condor_for_post.py` according to you own settings

```bash
cd condor_for_mc
python condor_for_postproc.py -f input.json
```
The production code is prepared for generating private signal samples
## <span id="Crab-mode"> Crab mode </span>
Crab mode is designed for data/MC.

```bash
cd crab
```
The crab mode is based on official nanotools. See reference: <https://github.com/cms-nanoAOD/nanoAOD-tools/tree/master/crab>

The `crab_help.py` is designed to simplify the repeated process. And the `input.json` is a sample for how to provide input for `crab_help.py`. `WZG_crab_script.sh` is the executed code on crab and will call the WZG_selector for postprocessing. 

First you need to generate the cfg file for crab job.
```bash
python3 crab_help.py -f input.json -m prepare
```
It will create a folder that with cfg files inside automatically. Noticed that some paths in `crab_help.py` need to be changed according to different user.

Then you can submit crab jobs with:
```bash
python3 crab_help.py -f input.json -m submit
```
Similarly, you can use `-m status`, `-m resubmit`, `-m kill` to batchly operate crab jobs.
