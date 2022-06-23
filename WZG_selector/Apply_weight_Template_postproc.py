#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

from PhysicsTools.NanoAODTools.postprocessing.modules.FakeLep_Apply_weight_Template_Module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.FakePho_Apply_weight_Template_Module import *

import argparse
import re
import optparse


parser = argparse.ArgumentParser(description='create attachment NanoAOD-like fake lepton result')
parser.add_argument('-f', dest='file', default='', help='File input')
parser.add_argument('-y', dest='year', default='2018', help='year')
args = parser.parse_args()

if args.year == '2018':
    Modules = [ApplyWeightFakeLeptonModule_18(),ApplyWeightFakePhotonModule18()]
elif args.year == '2017':
    Modules = [ApplyWeightFakeLeptonModule_17(),ApplyWeightFakePhotonModule17()]
    
infilelist = [args.file]
jsoninput = None
fwkjobreport = False


p=PostProcessor(".",infilelist,
                branchsel="Apply_weight_keep_and_drop.txt",
                modules=Modules,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                provenance=True,
                outputbranchsel="Apply_weight_output_branch_selection.txt",
                )
p.run()