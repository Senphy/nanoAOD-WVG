#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2       import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from full_Template_Module import * 

import argparse
import re
import optparse


parser = argparse.ArgumentParser(description='fake photon full template production')
parser.add_argument('-f', dest='file', default='', help='File input. In local mode it will be the filepath. In condor mode it will be the dataset name')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
parser.add_argument('-p', dest='period',default="B", help="Run period, only work for data")
args = parser.parse_args()

# print ("mode: ", args.mode)
# print ("input file: ", args.file)


if args.isdata:
    if args.year == '2018':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2018", runPeriod=args.period, metBranchName="MET")
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2017", runPeriod=args.period, metBranchName="MET")
    if args.year == '2016':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016", runPeriod=args.period, metBranchName="MET")
    if args.year == '2016_PreVFP':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016_PreVFP", runPeriod=args.period, metBranchName="MET")
    Modules = [countHistogramsProducer(),jetmetCorrector(),FakePhotonFullModule()]
else:
    if args.year == '2018':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2018", jesUncert="All", metBranchName="MET", splitJER=True, applyHEMfix=True)
        Modules = [countHistogramsProducer(),jetmetCorrector(),FakePhotonFullModule(),puWeight_2018()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2017", jesUncert="All", metBranchName="MET", splitJER=True)
        Modules = [countHistogramsProducer(),PrefCorr(),jetmetCorrector(),FakePhotonFullModule(),puWeight_2017()]
    if args.year == '2016':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016", jesUncert="All", metBranchName="MET", splitJER=True)
        Modules = [countHistogramsProducer(),PrefCorr(),jetmetCorrector(),FakePhotonFullModule(),puWeight_2016()]
    if args.year == '2016_PreVFP':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016_PreVFP", jesUncert="All", metBranchName="MET", splitJER=True)
        Modules = [countHistogramsProducer(),PrefCorr(),jetmetCorrector(),FakePhotonFullModule(),puWeight_2016()]

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
                branchsel="full_keep_and_drop.txt",
                modules=Modules,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                provenance=True,
                outputbranchsel="full_output_branch_selection.txt",
                )
p.run()