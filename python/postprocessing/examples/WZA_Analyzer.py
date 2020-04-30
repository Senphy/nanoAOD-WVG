#!/usr/bin/env python
# Analyzer for WZG Analysis based on nanoAOD tools

import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

test=0
MET_pass = 0
photon_pass = 0
electron_pass = 0
muon_pass = 0
lepton_pass = 0
threelepton_pass = 0
dilepton_pass = 0
emumu_pass = 0
btagjet_pass = 0
class WZAAnalysis(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("event",  "i")
        self.out.branch("MET",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("electron_pt",  "F")
        self.out.branch("muon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("electron_eta",  "F")
        self.out.branch("muon_eta",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("electron_phi",  "F")
        self.out.branch("muon_phi",  "F")
        self.out.branch("dilepton_mass",  "F")
        self.out.branch("Generator_weight","F")
        self.out.branch("max_CMVA","F")
        self.out.branch("max_CSVV2","F")
        self.out.branch("max_DeepB","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        jet_select = [] 
        dileptonp4 = ROOT.TLorentzVector()
        photon_select = []
        electron_select = []
        muon_select = [] 
        # Record the pass numbers for each cut. Noticed that for efficiency, those who can't pass the MET cut may not be counted because it will pass to next event directly.

        # dilepton = False
        emumu_dilepton = False  #emumu channal selection
        global MET_pass
        global photon_pass
        global electron_pass
        global muon_pass
        global lepton_pass
        global threelepton_pass
        global dilepton_pass
        global emumu_pass 
        global btagjet_pass
        global test

        # selection on MET. Pass to next event directly if fail.
        if  event.MET_pt>20:
            self.out.fillBranch("MET",event.MET_pt)
            MET_pass += 1
        else:
            return False  

        # selection on photons
        for i in range(0,len(photons)):
            if  photons[i].pt>20  and  abs(photons[i].eta)<2.5  and  photons[i].cutBased>=3: 
                photon_select.append(i)
        if len(photon_select)==0:
            return False                        #reject event if there is no photon selected in the event
        else:
            photon_pass += 1

        # selection on electrons
        for i in range(0,len(electrons)):
            if  electrons[i].pt>20  and  abs(electrons[i].eta)<2.5  and  electrons[i].cutBased>=3:
                electron_pass += 1
                electron_select.append(i)

        #selection on muons
        for i in range(0,len(muons)):
            if  muons[i].pt>20  and  abs(muons[i].eta)<2.5:  #or  muons[i].cutBased<=3:            
                muon_pass += 1
                muon_select.append(i)

        if len(electron_select)==0 and len(muon_select)==0:      #reject event if there is no lepton selected in the event
            return False
        else:
            lepton_pass += 1
        
        if len(electron_select)+len(muon_select) != 3:      #reject event if there are not exactly three leptons
            return False
        else:
            threelepton_pass += 1

        #dilepton mass
        if  len(muon_select)==2  and len(electron_select)==1:  #begin with emumu channel 
            if muons[muon_select[0]].pdgId == -muons[muon_select[1]].pdgId:
                dileptonmass = -1.0
                dileptonmass = (muons[muon_select[0]].p4()+muons[muon_select[1]].p4()).M()
                # if dileptonmass >= 60 and dileptonmass <= 120:
                print "a=",photon_select, "e=",electron_select, "mu=",muon_select
                emumu_dilepton = True

        if emumu_dilepton == False: 
            return False                        #reject event if there are no di-leptons pass the selection in the event 
        else:
            emumu_pass += 1

        # selection on b-tag jet
        for i in range(0,len(jets)): 
            btag_cut = False
            if jets[i].btagCMVA > -0.5884:  # cMVAv2L
            # if jets[i].btagCMVA > 0.4432:  # cMVAv2M
            # if jets[i].btagCSVV2 > 0.5426:  # CSVv2L
            # if jets[i].btagCSVV2 > 0.8484:  # CSVv2M
            # if jets[i].btagDeepB > 0.2219:  # DeepCSVL
            # if jets[i].btagDeepB > 0.6324:  # DeepCSVM
                btag_cut = True      #initialize
                if jets[i].pt<30:
                    continue
                for j in range(0,len(photon_select)):          # delta R cut, if all deltaR(lep,jet) and deltaR(gamma,jet)>0.3, consider jet as a b jet
                    if deltaR(jets[i].eta,jets[i].phi,photons[photon_select[j]].eta,photons[photon_select[j]].phi) < 0.3:
                        btag_cut = False
                for j in range(0,len(electron_select)):
                    if deltaR(jets[i].eta,jets[i].phi,electrons[electron_select[j]].eta,electrons[electron_select[j]].phi) < 0.3:
                        btag_cut = False
                for j in range(0,len(muon_select)):
                    if deltaR(jets[i].eta,jets[i].phi,muons[muon_select[j]].eta,muons[muon_select[j]].phi) < 0.3:
                        btag_cut = False
            if btag_cut == True:
                return False
        btagjet_pass += 1

        # max_CMVA=-999
        # max_CSVV2=-999
        # max_DeepB=-999
        # for i in range(0,len(jets)): 
        #     if jets[i].btagCMVA > max_CMVA: max_CMVA = jets[i].btagCMVA
        #     if jets[i].btagCSVV2 > max_CSVV2: max_CSVV2 = jets[i].btagCSVV2
        #     if jets[i].btagDeepB > max_DeepB: max_DeepB = jets[i].btagDeepB
        # self.out.fillBranch("max_CMVA",max_CMVA)
        # self.out.fillBranch("max_CSVV2",max_CSVV2)
        # self.out.fillBranch("max_DeepB",max_DeepB)



        for i in range(0,len(photon_select)):
            self.out.fillBranch("photon_pt",photons[photon_select[i]].pt)
            self.out.fillBranch("photon_eta",photons[photon_select[i]].eta)
            self.out.fillBranch("photon_phi",photons[photon_select[i]].phi)
        for i in range(0,len(electron_select)):
            self.out.fillBranch("electron_pt",electrons[electron_select[i]].pt)
            self.out.fillBranch("electron_eta",electrons[electron_select[i]].eta)
            self.out.fillBranch("electron_phi",electrons[electron_select[i]].phi)
        for i in range(0,len(muon_select)):
            self.out.fillBranch("muon_pt",muons[muon_select[i]].pt)
            self.out.fillBranch("muon_eta",muons[muon_select[i]].eta)
            self.out.fillBranch("muon_phi",muons[muon_select[i]].phi)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("dilepton_mass",dileptonmass)
        self.out.fillBranch("Generator_weight",event.Generator_weight)
        return True

# files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/EE33CA79-B0A1-1145-A457-FE7B7C1A03BC.root"]
# files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/356CFA55-E91B-1940-ACFC-FE3E769A44D5.root"]
# files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/260000/FA76270A-417C-174F-B403-8FE5E5A3EFE4.root"]
# files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/ttZJets_13TeV_madgraphMLM/NANOAODSIM/Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/280000/AF15D61D-C169-1F49-B287-DCF0B7F44B8B.root"]
# files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/tZq_ll_4f_13TeV-amcatnlo-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/280000/A85C5B62-D4C8-6845-B005-C0CE9B0AB4EA.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/bwcutoff_15_test_submit/10k/SMP-RunIISummer16NanoAODv6-00310.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/bwcutoff_30_test_submit/10k/SMP-RunIISummer16NanoAODv6-00310.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/background/TTWJetsToLNu.root"]
# files=["/afs/cern.ch/work/s/sdeng/config_file/background/TTZJets.root"]
files=["/afs/cern.ch/work/s/sdeng/config_file/background/tZq_ll.root"]
p=PostProcessor(".",files,branchsel="input_branch_sel.txt",modules=[countHistogramsProducer(),WZAAnalysis()],provenance=True,outputbranchsel="output_branch_sel.txt")
p.run()

print "MET_pass","\t","=","\t",MET_pass
print "photon_pass","\t","=","\t",photon_pass
# print "electron_pass","\t","=","\t",electron_pass
# print "muon_pass","\t","=","\t",muon_pass 
print "lepton_pass","\t","=","\t",lepton_pass
print "threelepton_pass","\t","=","\t",threelepton_pass
print "emumu_pass","\t","=","\t",emumu_pass
print "btagjet_pass","\t","=","\t",btagjet_pass