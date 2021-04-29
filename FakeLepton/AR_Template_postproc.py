#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

# from WZG_Module import * 
from AR_Template_Module import *

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
    Modules = [countHistogramsProducer(),ApplyRegionFakeLeptonModule()]
    print "processing data"
else:
    Modules = [countHistogramsProducer(),ApplyRegionFakeLeptonModule()]
    # Modules = [countHistogramsProducer(),ApplyRegionFakeLeptonModule(),puWeight_2018(),PrefCorr()]
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
                branchsel="AR_keep_and_drop.txt",
                modules=Modules,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                provenance=True,
                outputbranchsel="AR_output_branch_selection.txt",
                )
p.run()