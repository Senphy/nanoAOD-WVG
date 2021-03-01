#!/usr/bin/env python
from __future__ import absolute_import
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

# from WZG_Module import * 
import WZG_Module_data as WZG

import argparse
import re
import optparse
sys.path.append('../WZG_selector')
import DAS_filesearch as search
import json


parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f',dest='file',help='input file, if it is not provided, assume as a crab job',default=None)
parser.add_argument('-y',dest='year',help='the year or data',choices=('2016','2017','2018'),default='2018')
args = parser.parse_args()

if args.file:
    files = [args.file]
    jsoninput = None
    fwkjobreport = False
else:
    files = inputFiles()
    jsoninput = runsAndLumis()
    fwkjobreport = True

print "Input root file: ", files 

# condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
# designed for single file here in order to run in parallel
# local specific file input, also support root://xxx    

p=PostProcessor(".",files,
                branchsel="WZG_input_branch.txt",
                modules=[countHistogramsProducer(),WZG.WZG_Producer()],
                provenance=True,
                outputbranchsel="WZG_output_branch.txt",
                jsonInput=jsoninput, 
                fwkJobReport=fwkjobreport
                )
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
print "total processed events","\t","=","\t",WZG.test
