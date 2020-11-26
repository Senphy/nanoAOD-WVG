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
import DAS_filesearch as search


parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='file', default='', help='local file input')
parser.add_argument('-y', dest='year', default='2016', help='year of dataset')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-n', dest='name', default='test', help='dataset name in short, currently support' 
    '\n tZq_ll'
    '\n WZ'
    '\n TTWJetsToLNu'
    '\n ttZJets')
args = parser.parse_args()

print "mode: ", args.mode
print "year: ", args.year
print "dataset_name: ", args.name




# classify input files
if args.file == '':

    print "no local file input, use DAS file"
    dataset = ''
    if args.name == 'tZq_ll':
        if args.year == '2016': dataset = "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
    elif args.name == 'WZ':
        if args.year == '2016': dataset = "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
    elif args.name == 'TTWJetsToLNu':
        if args.year == '2016': dataset = "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
    elif args.name == 'ttZJets':
        if args.year == '2016': dataset = "/ttZJets_13TeV_madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
    else:
        print "unknown dataset name"
        sys.exit(0)


    files = []

    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    if 'condor' in args.mode:
        pass

    else:
        search.getFilePath(dataset, args.name+"_"+args.year)

    with open("filepath_"+args.name+"_"+args.year+".txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            files.append(line)

    print 'from DAS input files: ',files

    p=PostProcessor(".",files,branchsel="WZG_input_branch.txt",modules=[countHistogramsProducer(),WZG.WZG_Producer()],provenance=True,outputbranchsel="WZG_output_branch.txt")
    p.run()


else:    
    files = []
    # condor can't use dasgoclient, so we should upload the filepath for condor run. sth. different with local run here
    # designed for single file here in order to run in parallel
    if 'condor' in args.mode:
        files.append(args.file)
        print 'input files: ',files
        print 'test'

    # local specific file input, also support root://xxx    
    else:
        if not ',' in args.file:
            files.append(args.file)

        else:
            for i in args.file.split(','):
                files.append(i)

        print 'input files: ',files

    p=PostProcessor(".",files,branchsel="WZG_input_branch.txt",modules=[countHistogramsProducer(),WZG.WZG_Producer()],provenance=True,outputbranchsel="WZG_output_branch.txt")
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
