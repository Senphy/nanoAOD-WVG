
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
import numpy as np


class HEM_check_Producer(Module):
    def __init__(self, year):
        self.year = year
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("hem_nbJets", "i")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        selected_photons = [event.TightPhotons_index[i] for i in range(event.nTightPhotons)]
        selected_electrons = [event.TightElectrons_index[i] for i in range(event.nTightElectrons)]
        selected_muons = [event.TightMuons_index[i] for i in range(event.nTightMuons)]

        if hasattr(event, 'MET_T1Smear_pt_jesHEMIssueUp'):
            pass

        hem_tight_bjets = []
        for i in range(0, len(jets)):
            if hasattr(event, 'Jet_pt_jesHEMIssueDown'):
                if event.Jet_pt_jesHEMIssueDown[i] < 30:
                    continue
            else:
                if jets[i].pt < 30:
                    continue

            if abs(jets[i].eta) > 2.4:
                continue

            if not jets[i].jetId == 6:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(selected_photons)):
                if deltaR(jets[i].eta,jets[i].phi,photons[selected_photons[j]].eta,photons[selected_photons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(selected_electrons)):
                if deltaR(jets[i].eta,jets[i].phi,electrons[selected_electrons[j]].eta,electrons[selected_electrons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(selected_muons)):
                if deltaR(jets[i].eta,jets[i].phi,muons[selected_muons[j]].eta,muons[selected_muons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut: 
                continue

            # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
            # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
            # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD#Jets
            # tightLepVeto PF jets (ak4), UL 2016/2017/2018 (jetId 110=6), medium B-tag WP
            # UL17 DeepCSV=(nanoaod btagDeepB) loose: 0.1355, medium: 0.4506, tight: 0.7738
            # UL18 DeepCSV=(nanoaod btagDeepB) loose: 0.1208, medium: 0.4168, tight: 0.7665
            # UL17 DeepFlavor=(nanoaod btagDeepFlavB) loose: 0.0532, medium: 0.3040, tight: 0.7476
            # UL18 DeepFlavor=(nanoaod btagDeepFlavB) loose: 0.0490, medium: 0.2783, tight: 0.7100

            # c-jet tag is based on two-D cuts, medium DeepJet WP:
            # UL17 CvsL=btagDeepFlavCvL: 0.085, CvsB=btagDeepFlavCvB: 0.34
            # UL18 CvsL=btagDeepFlavCvL: 0.099, CvsB=btagDeepFlavCvB: 0.325
            # c-tag not available in NANOAOD yet

            if self.year == '2016Pre':
                if jets[i].btagDeepB > 0.8819:
                    hem_tight_bjets.append(i)
            elif self.year == '2016Post':
                if jets[i].btagDeepB > 0.8767:
                    hem_tight_bjets.append(i)
            elif self.year == '2017':
                if jets[i].btagDeepB > 0.7738:
                    hem_tight_bjets.append(i)
            elif self.year == '2018':
                if jets[i].btagDeepB > 0.7665:
                    hem_tight_bjets.append(i)
        self.out.fillBranch("hem_nbJets", len(hem_tight_bjets))

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

HEM_check_Module_16Pre = lambda : HEM_check_Producer('2016Pre')
HEM_check_Module_16Post = lambda : HEM_check_Producer('2016Post')
HEM_check_Module_17 = lambda : HEM_check_Producer('2017')
HEM_check_Module_18 = lambda : HEM_check_Producer('2018')