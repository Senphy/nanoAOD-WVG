import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-i',dest='infile',help="if an input file is not provide, assume this is a crab job")
parser.add_argument('-d',dest='isdata',action='store_true',default=False)

args = parser.parse_args()

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  FR_Template_Module import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

if args.isdata:
    modules = [countHistogramsModule(),FakeLeptonModule()]
else:
    modules = [countHistogramsModule(),FakeLeptonModule(),puWeight_2018(),PrefCorr()]

if args.infile:
    infilelist = [args.infile]
    jsoninput = None
    fwkjobreport = False
else:
    # from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    infilelist = inputFiles()
    # jsoninput = runsAndLumis()
    fwkjobreport = True

p=PostProcessor(".",infilelist,
                None,
                branchsel="FR_keep_and_drop.txt",
                modules,
                provenance=True,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                # jsonInput=jsoninput, 
                outputbranchsel = "FR_output_branch_selection.txt")

p.run()

print "DONE"