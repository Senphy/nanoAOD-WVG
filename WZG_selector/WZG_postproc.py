#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2       import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleRECOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleIDSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonIDISOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btagWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.photonIDSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btagEffProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btagWeightProducer_1a import *
from PhysicsTools.NanoAODTools.postprocessing.modules.define_object import *
from PhysicsTools.NanoAODTools.postprocessing.modules.pre_select import *
from PhysicsTools.NanoAODTools.postprocessing.modules.WZG_Module_multi import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.FakeLep_Apply_weight_Template_Module import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.FakePho_Apply_weight_Template_Module import *

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
        Modules = [muonScaleRes2018(),pre_select_Producer(),jetmetCorrector(),define_object_Module_18(),WZG_select_multi_Module()]
        # Modules = [muonScaleRes2018(),first_Template_Module(),jetmetCorrector(),WZG_select_Module_18()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2017", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2017(),pre_select_Producer(),jetmetCorrector(),define_object_Module_17(),WZG_select_multi_Module()]
    if args.year == '2016Post':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2016b(),pre_select_Producer(),jetmetCorrector(),define_object_Module_16Post(),WZG_select_multi_Module()]
    if args.year == '2016Pre':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016_preVFP", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2016a(),pre_select_Producer(),jetmetCorrector(),define_object_Module_16Pre(),WZG_select_multi_Module()]
else:
    if args.year == '2018':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2018", jesUncert="Total", metBranchName="MET", splitJER=False, applyHEMfix=True)
        Modules = [countHistogramsProducer(),muonScaleRes2018(),pre_select_Producer(),puAutoWeight_2018(),muonIDISOSF2018(),eleRECOSF2018(),eleIDSF2018(),phoIDSF2018(),jetmetCorrector(),btagSFUL2018(),define_object_Module_18(),btagEffModule(),WZG_select_multi_Module()]
        # Modules = [countHistogramsProducer(),muonScaleRes2018(),first_Template_Producer(),puAutoWeight_2018(),muonIDISOSF2018(),eleRECOSF2018(),eleIDSF2018(),phoIDSF2018(),jetmetCorrector(),btagSFUL2018(),btagWeightModule_18(),WZG_select_Module_18()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2017", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),muonScaleRes2017(),pre_select_Producer(),puAutoWeight_2017(),PrefCorrUL17(),muonIDISOSF2017(),eleRECOSF2017(),eleIDSF2017(),phoIDSF2017(),jetmetCorrector(),btagSFUL2017(),define_object_Module_17(),btagEffModule(),WZG_select_multi_Module()]
    if args.year == '2016Post':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),muonScaleRes2016b(),pre_select_Producer(),puAutoWeight_2016(),PrefCorrUL16_postVFP(),muonIDISOSF2016(),eleRECOSF2016(),eleIDSF2016(),phoIDSF2016Post(),jetmetCorrector(),btagSFUL2016Post(),define_object_Module_16Post(),btagEffModule(),WZG_select_multi_Module()]
    if args.year == '2016Pre':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016_preVFP", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),muonScaleRes2016a(),pre_select_Producer(),puAutoWeight_2016(),PrefCorrUL16_preVFP(),muonIDISOSF2016(),eleRECOSF2016(),eleIDSF2016(),phoIDSF2016Pre(),jetmetCorrector(),btagSFUL2016Pre(),define_object_Module_16Pre(),btagEffModule(),WZG_select_multi_Module()]

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

if args.isdata and args.year=='2018' and args.period=='D' and ('MuonEG' in infilelist):
    print 'special treatment for MuonEG_Run2018D'
    import FWCore.PythonUtilities.LumiList as LumiList
    import FWCore.ParameterSet.Config as cms

    lumisToProcess = cms.untracked.VLuminosityBlockRange( LumiList.LumiList(filename="./Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt").getCMSSWString().split(',') )
    # print lumisToProcess

    runsAndLumis_special = {}
    for l in lumisToProcess:
        if "-" in l:
            start, stop = l.split("-")
            rstart, lstart = start.split(":")
            rstop, lstop = stop.split(":")
        else:
            rstart, lstart = l.split(":")
            rstop, lstop = l.split(":")
        if rstart != rstop:
            raise Exception(
                "Cannot convert '%s' to runs and lumis json format" % l)
        if rstart not in runsAndLumis_special:
            runsAndLumis_special[rstart] = []
        runsAndLumis_special[rstart].append([int(lstart), int(lstop)])
    jsoninput = runsAndLumis_special

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