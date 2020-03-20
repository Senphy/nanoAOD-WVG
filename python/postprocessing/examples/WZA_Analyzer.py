#!/usr/bin/env python
import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

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

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        # jets = Collection(event, "Jet")
        # Jet_select = ROOT.TLorentzVector()
        photon_select = []
        electron_select = []
        muon_select = [] 

        dilepton = False

        # selection on MET
        if  event.MET_pt>20  and  event.MET_pt<30:
            self.out.fillBranch("MET",event.MET_pt)
        else:
            return False  

        # selection on photons
        for i in range(0,len(photons)):
            if  photons[i].pt>30  and  abs(photons[i].eta)<1.44  and  photons[i].cutBased>=3: #pt eta ID cut
                photon_select.append(i)

        # selection on electrons
        for i in range(0,len(electrons)):
            # print event.event
            if  electrons[i].pt>30  and  abs(electrons[i].eta)<2.5  and  electrons[i].cutBased>=3: #pt eta ID cut
                electron_select.append(i)
            if i != len(electrons) and dilepton == False:
                for j in range(i+1,len(electrons)):
                    if electrons[i].pdgId == -electrons[j].pdgId:
                        # print electrons[i].mass," + ",electrons[j].mass," = ",electrons[i].mass+electrons[j].mass
                        if abs(electrons[i].mass+electrons[j].mass)*1000 >= 60 and abs(electrons[i].mass+electrons[j].mass)*1000 <= 120:
                            dilepton = True                                                      #dilepton selection
                            break

        #selection on muons
        for i in range(0,len(muons)):
            if  muons[i].pt>25  and  abs(muons[i].eta)<2.1:  #or  muons[i].cutBased<=3:             #pt eta ID cut
                muon_select.append(i)
            if i != len(muons) and dilepton == False:
                for j in range(i+1,len(muons)):
                    if muons[i].pdgId == -muons[j].pdgId:
                        if abs(muons[i].mass+muons[j].mass)*1000 >= 60 and abs(muons[i].mass+muons[j].mass)*1000 <= 120:
                            dilepton = True                                                      #dilepton selection
                            break

        if dilepton == False: return False        #reject events
        if len(photon_select)==0: return False
        if len(electron_select)==0 and len(muon_select)==0: return False

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

        return True

# files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/EE33CA79-B0A1-1145-A457-FE7B7C1A03BC.root"]
files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/356CFA55-E91B-1940-ACFC-FE3E769A44D5.root"]
p=PostProcessor(".",files,branchsel="input_branch_sel.txt",modules=[WZAAnalysis()],provenance=True,outputbranchsel="output_branch_sel.txt")
p.run()