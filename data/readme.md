need to move this folder to Nanotools `python/postprocessing` and compile
```bash
cp -r * $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/data/
cd $CMSSW_BASE/src
scram b -j10
```