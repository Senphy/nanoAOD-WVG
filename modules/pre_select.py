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


class pre_select_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.h_cutflow_pre_select = ROOT.TH1D('h_cutflow_pre_select','h_cutflow_pre_select',1,0,1)
        self.h_cutflow_1ossf = ROOT.TH1D('h_cutflow_1ossf','h_cutflow_1ossf',1,0,1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_cutflow_pre_select.Write()
        self.h_cutflow_1ossf.Write()
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        tight_muons = []
        tight_electrons = []
        fake_muons = []
        fake_electrons = []
        veto_muons = []
        veto_electrons = []

        #selection on muons
        for i in range(0,len(muons)):
            if event.Muon_corrected_pt[i] < 15:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].tightId and muons[i].pfRelIso04_all < 0.4:
                fake_muons.append(i)
            elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
                veto_muons.append(i)
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())

        # selection on electrons
        for i in range(0,len(electrons)):
            if electrons[i].pt < 15:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased == 1:
                    fake_electrons.append(i)
                elif electrons[i].cutBased > 1:
                    veto_electrons.append(i)
        
        nleptons = len(tight_electrons) + len(tight_muons) + len(fake_muons) + len(fake_electrons)
        ntightleptons = len(tight_electrons) + len(tight_muons)
        # pre selection
        if nleptons < 2:
            self.h_cutflow_pre_select.Fill(1)
            return False

        if ntightleptons > 4:
            self.h_cutflow_pre_select.Fill(1)
            return False

        if nleptons == 2:
            # OSSF requirement
            if (len(tight_electrons) + len(fake_electrons) == 1) or (len(tight_muons) + len(fake_muons) == 1):
                self.h_cutflow_1ossf.Fill(1)
                return False
            if len(tight_muons)+len(fake_muons) == 2:
                selected_muons = tight_muons + fake_muons
                if muons[selected_muons[0]].pdgId == muons[selected_muons[1]].pdgId:
                    self.h_cutflow_1ossf.Fill(1)
                    return False
            if len(tight_electrons)+len(fake_electrons) == 2:
                selected_electrons = tight_electrons + fake_electrons
                if electrons[selected_electrons[0]].pdgId == electrons[selected_electrons[1]].pdgId:
                    self.h_cutflow_1ossf.Fill(1)
                    return False
        
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

pre_select_Module = lambda : pre_select_Producer()