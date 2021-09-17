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
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_lepton_weight",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Open the root file with 2D pt-eta fake rate
        file_ele = ROOT.TFile("%s/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/plot/Fake_Lepton/Ele_Fake_Rate_2D.root" % os.environ['CMSSW_BASE'],"READ")
        file_mu = ROOT.TFile("%s/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/plot/Fake_Lepton/Mu_Fake_Rate_2D.root" % os.environ['CMSSW_BASE'],"READ") 

        FR_E = file_ele.Get("fake_rate_e")
        FR_M = file_mu.Get("fake_rate_mu")

        weight = 1
        number_of_loose = event.nLooseMuon + event.nLooseElectron

        for i in range(0, len(event.LooseNotTightMuon_pt)):
            BinX = FR_M.GetXaxis().FindBin(abs(event.LooseNotTightMuon_eta[i]))
            BinY = FR_M.GetYaxis().FindBin(abs(event.LooseNotTightMuon_pt[i]))
            if BinX > FR_M.GetNbinsX():
                BinX = FR_M.GetNbinsX()
            if BinY > FR_M.GetNbinsY():
                BinY = FR_M.GetNbinsY()
            weight = weight*FR_M.GetBinContent(BinX, BinY)/(1 - FR_M.GetBinContent(BinX, BinY))
            
        for i in range(0, len(event.LooseNotTightElectron_pt)):
            BinX = FR_E.GetXaxis().FindBin(abs(event.LooseNotTightElectron_eta[i]))
            BinY = FR_E.GetYaxis().FindBin(abs(event.LooseNotTightElectron_pt[i]))
            if BinX > FR_E.GetNbinsX():
                BinX = FR_E.GetNbinsX()
            if BinY > FR_E.GetNbinsY():
                BinY = FR_E.GetNbinsY()
            weight = weight*FR_E.GetBinContent(BinX, BinY)/(1 - FR_E.GetBinContent(BinX, BinY))

        if (number_of_loose % 2 > 0):
            weight = weight
        else:
            weight = -weight
        self.out.fillBranch("fake_lepton_weight", weight)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakeLeptonModule = lambda : ApplyWeightFakeLeptonProducer()