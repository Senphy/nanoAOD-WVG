import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f',dest='infile',help="if an input file is not provide, assume this is a crab job")
parser.add_argument('-d',dest='isdata',action='store_true',default=False)
parser.add_argument('-y', dest='year', default='2018', help='year')

args = parser.parse_args()

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.modules.FakeLep_FR_Template_Module import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2       import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleRECOSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.eleIDSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.muonIDISOSFProducer import *

parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='File input. In local mode it will be the filepath. In condor mode it will be the dataset name')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-y', dest='year', default='2018', help='year')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
parser.add_argument('-p', dest='period',default="B", help="Run period, only work for data")
args = parser.parse_args()

PrefCorrUL16_preVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016preVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016preVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL16_postVFP = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2016postVFP", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2016postVFP", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])
PrefCorrUL17 = lambda : PrefCorr(jetroot="L1PrefiringMaps.root", jetmapname="L1prefiring_jetptvseta_UL2017BtoF", photonroot="L1PrefiringMaps.root", photonmapname="L1prefiring_photonptvseta_UL2017BtoF", branchnames=["PrefireWeight","PrefireWeight_Up", "PrefireWeight_Down"])

if args.isdata:
    if args.year == '2018':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2018", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2018(),FRFakeLep_first_Template_Module(),jetmetCorrector(),FRFakeLeptonModule()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2017", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2017(),FRFakeLep_first_Template_Module(),jetmetCorrector(),FRFakeLeptonModule()]
    if args.year == '2016':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2016b(),jetmetCorrector(),FRFakeLeptonModule()]
    if args.year == '2016_PreVFP':
        jetmetCorrector = createJMECorrector(isMC=False, dataYear="UL2016_PreVFP", runPeriod=args.period, metBranchName="MET")
        Modules = [muonScaleRes2016a(),jetmetCorrector(),FRFakeLeptonModule()]
else:
    if args.year == '2018':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2018", jesUncert="Total", metBranchName="MET", splitJER=False, applyHEMfix=True)
        Modules = [countHistogramsProducer(),muonScaleRes2018(),FRFakeLep_first_Template_Module(),puAutoWeight_2018(),muonIDISOSF2018(),eleRECOSF2018(),eleIDSF2018(),jetmetCorrector(),FRFakeLeptonModule()]
    if args.year == '2017':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2017", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),muonScaleRes2017(),FRFakeLep_first_Template_Module(),puAutoWeight_2017(),PrefCorrUL17(),muonIDISOSF2017(),eleRECOSF2017(),eleIDSF2017(),jetmetCorrector(),FRFakeLeptonModule()]
    if args.year == '2016':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),puAutoWeight_2016(),PrefCorrUL16_postVFP(),muonIDISOSF2016(),muonScaleRes2016b(),eleRECOSF2016(),eleIDSF2016(),jetmetCorrector(),FRFakeLeptonModule()]
    if args.year == '2016_PreVFP':
        jetmetCorrector = createJMECorrector(isMC=True, dataYear="UL2016_PreVFP", jesUncert="Total", metBranchName="MET", splitJER=False)
        Modules = [countHistogramsProducer(),puAutoWeight_2016(),PrefCorrUL16_preVFP(),muonIDISOSF2016(),muonScaleRes2016a(),eleRECOSF2016(),eleIDSF2016(),jetmetCorrector(),FRFakeLeptonModule()]

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
                branchsel="FR_keep_and_drop.txt",
                modules = Modules,
                provenance=True,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                outputbranchsel = "FR_output_branch_selection.txt")

p.run()