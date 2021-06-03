#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

# from WZG_Module import * 
import WZG_Module as WZG

import argparse
import re
import optparse


parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='File input. In local mode it will be the filepath. In condor mode it will be the dataset name')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
args = parser.parse_args()

print "mode: ", args.mode
print "input file: ", args.file


if args.isdata:
    Modules = [countHistogramsProducer(),WZG.WZG_Producer()]
    print "processing data"
else:
    if args.year == '2018':
        Modules = [countHistogramsModule(),WZG.WZG_Producer(),puWeight_2018()]
    if args.year == '2017':
        Modules = [countHistogramsModule(),WZG.WZG_Producer(),puWeight_2017(),PrefCorr()]
    if args.year == '2016':
        Modules = [countHistogramsModule(),WZG.WZG_Producer(),puWeight_2016(),PrefCorr()]
    print "processing MC samples"

if args.file:

    infilelist = []
    jsoninput = None
    fwkjobreport = False

    if args.mode == 'condor':
        import DAS_filesearch as search
        infilelist.append(search.getValidSite(args.file)+args.file) 
    else:
        infilelist = [args.file]

else:

    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    infilelist = inputFiles()
    jsoninput = runsAndLumis()
    fwkjobreport = True

p=PostProcessor(".",infilelist,
                branchsel="WZG_input_branch.txt",
                modules=Modules,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                provenance=True,
                outputbranchsel="WZG_output_branch.txt",
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
