
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


class first_Template_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nLooseLep","I") # actually means loose but not tight lep
        self.out.branch("nTightLep","I")
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        # photons = Collection(event, "Photon")
        tight_photons = []
        tight_electrons = [] 
        tight_muons = [] 
        loose_but_not_tight_muons = []
        loose_but_not_tight_electrons = []

        if event.nElectron + event.nMuon < 2:
            return False

        for i in range (0,len(muons)):
            if muons[i].pt < 10:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
                loose_but_not_tight_muons.append(i)

        for i in range(0,len(electrons)):
            if electrons[i].pt < 10:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        if len(loose_but_not_tight_muons) + len(loose_but_not_tight_muons) + len(tight_muons) + len(tight_electrons) < 2:
            return False

        if len(loose_but_not_tight_muons) + len(loose_but_not_tight_muons) + len(tight_muons) + len(tight_electrons) > 4:
            return False
        
        if len(tight_electrons) + len(tight_muons) > 4:
            return False

        self.out.fillBranch("nLooseLep", len(loose_but_not_tight_muons)+len(loose_but_not_tight_electrons))
        self.out.fillBranch("nTightLep", len(tight_muons)+len(tight_electrons))

        return True

class second_Template_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out.branch("MET","F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("photon_genPartFlav",  "I")
        self.out.branch("photon_mark",  "I")
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        # photons = Collection(event, "Photon")
        tight_photons = []
        tight_electrons = [] 
        tight_muons = [] 
        loose_but_not_tight_muons = []
        loose_but_not_tight_electrons = []

        if hasattr(event, "MET_T1Smear_pt"):
            self.out.fillBranch("MET",event.MET_T1Smear_pt)
        else:
            self.out.fillBranch("MET",event.MET_pt)

        for i in range (0,len(muons)):
            if muons[i].pt < 10:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].pfRelIso04_all < 0.4:
                loose_but_not_tight_muons.append(i)

        for i in range(0,len(electrons)):
            if electrons[i].pt < 10:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        if len(loose_but_not_tight_muons) + len(loose_but_not_tight_muons) + len(tight_muons) + len(tight_electrons) < 2:
            return False

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

first_Template_Module = lambda : first_Template_Producer()
second_Template_Module = lambda : second_Template_Producer()