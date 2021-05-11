import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f',dest='infile',help="if an input file is not provide, assume this is a crab job")
parser.add_argument('-d',dest='isdata',action='store_true',default=False)
parser.add_argument('-y', dest='year', default='2018', help='year')

args = parser.parse_args()

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  DY_Template_Module import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

if args.isdata:
    Modules = [countHistogramsModule(),DYTestModule()]
else:
    if args.year == '2018':
        Modules = [countHistogramsModule(),DYTestModule(),puWeight_2018(),PrefCorr()]
    if args.year == '2017':
        Modules = [countHistogramsModule(),DYTestModule(),puWeight_2017(),PrefCorr()]

if args.infile:
    infilelist = [args.infile]
    jsoninput = None
    fwkjobreport = False
else:
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    infilelist = inputFiles()
    jsoninput = runsAndLumis()
    fwkjobreport = True

p=PostProcessor(".",infilelist,
                branchsel="DY_keep_and_drop.txt",
                modules = Modules,
                provenance=True,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                outputbranchsel = "DY_output_branch_selection.txt")

p.run()