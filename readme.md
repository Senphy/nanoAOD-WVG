# WZG selector
Based on NanoAOD Tools: <https://github.com/cms-nanoAOD/nanoAOD-tools>

Dedicated for WZG analysis on lxplus environment

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
```
<br>

## <span id="Baseline-selection"> Baseline selection local test</span>
In WZG_seletor, `WZG_Module.py` is designed for basic selection (e.g. pt cut). Use `WZG_postproc.py` for local test.

```bash
python WZG_postproc.py -h
```

arguments:
- `-f`  specify the input file. For local file e.g. `/afs/xxx.root`. For DAS file e.g. `root://xxx`. In condor mode it should be dataset name e.g. /WZG/XXX/NanoAODSIM
- `-m`  Run mode. Normally use `local`. `condor` mode is designed as an interface for `condor_for_postproc.py` in condor folder.


`DAS_filesearch.py` is designed for returning LFN from given dataset. And store LFN into given filepath_GIVENFILENAME.txt. Then it will call `test_ValidSite_cfy.py` to search the valid site which can get access to the LFN.

<br>

## <span id="Condor-mode"> Condor mode </span>
Condor mode is designed for MC. 
In condor folder, `condor_for_postproc.py` is designed for preparing codes and submitting them to HTcondor. The purpose is to run over samples on DAS in parallel. It has `-f` arguments to load input json.

First you need to setup grid certification
```bash
voms-proxy-info -voms cms -valid 192:0
```
Modify `Proxy_path` in `condor_for_post.py` according to you own settings

```bash
python condor_for_postproc.py -f input.json
```
## <span id="Crab-mode"> Crab mode </span>
Crab mode is designed for data.


