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



class ApplyWeightFakeLeptonProducer(Module):
    def __init__(self,year):
        self.year = year
        if self.year == '2018':
            self.file_ele_path = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/Fake_Lepton/Ele_Fake_Rate_2D_2018_v9.root' % os.environ['CMSSW_BASE']
            self.file_mu_path ='%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/Fake_Lepton/Mu_Fake_Rate_2D_2018_v9.root' % os.environ['CMSSW_BASE']
        elif self.year == '2017':
            self.file_ele_path = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/Fake_Lepton/Ele_Fake_Rate_2D_2017_v9.root' % os.environ['CMSSW_BASE']
            self.file_mu_path = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/Fake_Lepton/Mu_Fake_Rate_2D_2017_v9.root' % os.environ['CMSSW_BASE']
        elif self.year == '2016':
            self.file_ele_path = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/Fake_Lepton/Ele_Fake_Rate_2D_2016.root' % os.environ['CMSSW_BASE']
            self.file_mu_path = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/Fake_Lepton/Mu_Fake_Rate_2D_2016.root' % os.environ['CMSSW_BASE']
        pass
    def beginJob(self):
        self.FR_E = ROOT.TH2F()
        self.FR_M = ROOT.TH2F()
        self.file_ele = ROOT.TFile.Open(self.file_ele_path)
        self.file_mu = ROOT.TFile.Open(self.file_mu_path)
        self.FR_E = self.file_ele.Get('fake_rate_e')
        self.FR_M = self.file_mu.Get('fake_rate_mu')
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_lepton_weight",  "F")
        self.out.branch("fake_lepton_weight_up",  "F")
        self.out.branch("fake_lepton_weight_down",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        # Open the root file with 2D pt-eta fake rate

        weight = 1
        weight_up = 1
        weight_down = 1
        number_of_loose = event.nFakeMuons + event.nFakeElectrons
        fake_muons = []
        fake_electrons = []
        if event.region_mark == 2: 
            for i in range(0, event.nFakeMuons):
                fake_muons.append(event.FakeMuons_index[i])
            for i in range(0, event.nFakeElectrons):
                fake_electrons.append(event.FakeElectrons_index[i])

            for i in fake_muons:
                BinX = self.FR_M.GetXaxis().FindBin(abs(muons[i].eta))
                BinY = self.FR_M.GetYaxis().FindBin(abs(event.Muon_corrected_pt[i]))
                if BinX > self.FR_M.GetNbinsX():
                    BinX = self.FR_M.GetNbinsX()
                if BinY > self.FR_M.GetNbinsY():
                    BinY = self.FR_M.GetNbinsY()
                temp_weight = self.FR_M.GetBinContent(BinX, BinY)
                temp_weight_err = self.FR_M.GetBinError(BinX, BinY)
                weight = weight*temp_weight/(1 - temp_weight)
                weight_up = weight_up*(temp_weight+temp_weight_err)/(1 - (temp_weight-temp_weight_err))
                weight_down = weight_down*(temp_weight-temp_weight_err)/(1 - (temp_weight+temp_weight_err))
                
            for i in fake_electrons:
                BinX = self.FR_E.GetXaxis().FindBin(abs(electrons[i].eta))
                BinY = self.FR_E.GetYaxis().FindBin(abs(electrons[i].pt))
                if BinX > self.FR_E.GetNbinsX():
                    BinX = self.FR_E.GetNbinsX()
                if BinY > self.FR_E.GetNbinsY():
                    BinY = self.FR_E.GetNbinsY()
                temp_weight = self.FR_E.GetBinContent(BinX, BinY)
                temp_weight_err = self.FR_E.GetBinError(BinX, BinY)
                weight = weight*temp_weight/(1 - temp_weight)
                weight_up = weight_up*(temp_weight+temp_weight_err)/(1 - (temp_weight-temp_weight_err))
                weight_down = weight_down*(temp_weight-temp_weight_err)/(1 - (temp_weight+temp_weight_err))

            if (number_of_loose % 2 > 0):
                weight = weight
            else:
                weight = -weight
        self.out.fillBranch("fake_lepton_weight", weight)
        self.out.fillBranch("fake_lepton_weight_up", weight_up)
        self.out.fillBranch("fake_lepton_weight_down", weight_down)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakeLeptonModule = lambda : ApplyWeightFakeLeptonProducer()
ApplyWeightFakeLeptonModule_17 = lambda : ApplyWeightFakeLeptonProducer("2017")
ApplyWeightFakeLeptonModule_18 = lambda : ApplyWeightFakeLeptonProducer("2018")
ApplyWeightFakeLeptonModule_16 = lambda : ApplyWeightFakeLeptonProducer("2016")