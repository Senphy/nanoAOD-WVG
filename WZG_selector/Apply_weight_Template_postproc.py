#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

from PhysicsTools.NanoAODTools.postprocessing.modules.FakeLep_Apply_weight_Template_Module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.FakePho_Apply_weight_Template_Module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btagWeightProducer_1a import *
from PhysicsTools.NanoAODTools.postprocessing.modules.theory_unc_Producer import *

import argparse
import re
import optparse


parser = argparse.ArgumentParser(description='create attachment NanoAOD-like fake lepton result')
parser.add_argument('-f', dest='file', default='', help='File input')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-d', dest='isdata', action='store_true', default=False, help='isdata')
args = parser.parse_args()

if str(args.year) == '2018':
    Modules = [ApplyWeightFakeLeptonModule_18(),ApplyWeightFakePhotonModule18()]
elif str(args.year) == '2017':
    Modules = [ApplyWeightFakeLeptonModule_17(),ApplyWeightFakePhotonModule17()]
elif str(args.year) == '2016Pre' or args.year == '2016Post':
    Modules = [ApplyWeightFakeLeptonModule_16(),ApplyWeightFakePhotonModule16()]
    
if not args.isdata:
    if str(args.year) == '2018':
        Modules.append(btagWeight_1a_Module_2018())
    elif str(args.year) == '2017':
        Modules.append(btagWeight_1a_Module_2017())
    elif str(args.year) == '2016Pre':
        Modules.append(btagWeight_1a_Module_2016Pre())
    elif str(args.year) == '2016Post':
        Modules.append(btagWeight_1a_Module_2016Post())
    Modules.append(theory_unc_Module())

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