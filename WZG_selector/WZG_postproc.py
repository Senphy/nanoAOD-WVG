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
from PhysicsTools.NanoAODTools.postprocessing.modules.eleRECOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleIDSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonIDISOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.WZG_Module import *

import argparse
import re
import optparse

PrefCorrUL16_preVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016preVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016preVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL16_postVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016postVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016postVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL17 = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2017BtoF", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2017BtoF", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])

parser = argparse.ArgumentParser(description='baseline selection')
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
        Modules = [muonScaleRes2018(),jetmetCorrector(),WZG_select_Module()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2017", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2017(),jetmetCorrector(),WZG_select_Module()]
    if args.year == '2016':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2016b(),jetmetCorrector(),WZG_select_Module()]
    if args.year == '2016_PreVFP':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016_PreVFP", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2016a(),jetmetCorrector(),WZG_select_Module()]
else:
    if args.year == '2018':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2018", jesUncert="Total", metBranchName="MET", splitJER=False, applyHEMfix=True)
        Modules = [countHistogramsProducer(),puAutoWeight_2018(),muonIDISOSF2018(),muonScaleRes2018(),eleRECOSF2018(),eleIDSF2018(),jetmetCorrector(),WZG_select_Module()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2017", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),puAutoWeight_2017(),PrefCorrUL17(),muonIDISOSF2017(),muonScaleRes2017(),eleRECOSF2017(),eleIDSF2017(),jetmetCorrector(),WZG_select_Module()]
    if args.year == '2016':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),puAutoWeight_2016(),PrefCorrUL16_postVFP(),muonIDISOSF2016(),muonScaleRes2016b(),eleRECOSF2016(),eleIDSF2016(),jetmetCorrector(),WZG_select_Module()]
    if args.year == '2016_PreVFP':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016_PreVFP", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),puAutoWeight_2016(),PrefCorrUL16_preVFP(),muonIDISOSF2016(),muonScaleRes2016a(),eleRECOSF2016(),eleIDSF2016(),jetmetCorrector(),WZG_select_Module()]

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