#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

# from WZG_Module import * 
import WZG_Module as WZG

# files=["/afs/cern.ch/work/s/sdeng/config_file/background/TTWJetsToLNu.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/background/TTZJets.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/background/WZ.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/background/tZq_ll.root"]

dataset = "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM" 
os.system("/cvmfs/cms.cern.ch/common/dasgoclient --query=\"file dataset="+dataset+"\" -limit=0")

files=["/eos/user/s/sdeng/WZG_analysis/final/2016/wza_full_60k.root"]
p=PostProcessor(".",files,branchsel="WZG_input_branch.txt",modules=[countHistogramsProducer(),WZG.WZG_Producer()],provenance=True,outputbranchsel="WZG_output_branch.txt")
p.run()

print "MET_pass","\t","=","\t",WZG.MET_pass
print "muon_pass","\t","=","\t",WZG.muon_pass 
print "electron_pass","\t","=","\t",WZG.electron_pass
print "photon_pass","\t","=","\t",WZG.photon_pass
print
print "none_photon_reject","\t","=","\t",WZG.none_photon_reject
print "none_lepton_reject","\t","=","\t",WZG.none_lepton_reject
print "none_3lepton_reject","\t","=","\t",WZG.none_3lepton_reject
print "same_charge_reject_eee","\t","=","\t",WZG.same_charge_reject_eee
print "same_charge_reject_mumumu","\t","=","\t",WZG.same_charge_reject_mumumu
print
print "emumu_pass","\t","=","\t",WZG.emumu_pass
print "muee_pass","\t","=","\t",WZG.muee_pass
print "eee_pass","\t","=","\t",WZG.eee_pass
print "mumumu_pass","\t","=","\t",WZG.mumumu_pass
print "btagjet_reject","\t","=","\t",WZG.btagjet_reject
print WZG.test
