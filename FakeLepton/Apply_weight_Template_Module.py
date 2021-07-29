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
        file_ele = ROOT.TFile("../plot/Fake_Lepton/Ele_Fake_Rate_2D.root","READ")
        file_mu = ROOT.TFile("../plot/Fake_Lepton/Mu_Fake_Rate_2D.root","READ") 

        if event.channel_mark == 1:
            FR_W = file_ele.Get("fake_rate_e")
            FR_Z = file_mu.Get("fake_rate_mu")
        elif event.channel_mark == 2:
            FR_W = file_mu.Get("fake_rate_mu")
            FR_Z = file_ele.Get("fake_rate_e")
        elif event.channel_mark == 3:
            FR_W = file_ele.Get("fake_rate_e")
            FR_Z = file_ele.Get("fake_rate_e")
        elif event.channel_mark == 4:
            FR_W = file_mu.Get("fake_rate_mu")
            FR_Z = file_mu.Get("fake_rate_mu")

        weight = [1,1,1]
        number_of_loose = 0

        if event.z_lepton1_type == 0:
            BinX = FR_Z.GetXaxis().FindBin(abs(event.z_lepton1_eta))
            BinY = FR_Z.GetYaxis().FindBin(abs(event.z_lepton1_pt))
            # handle overflow
            if BinX > FR_Z.GetNbinsX():
                BinX = FR_Z.GetNbinsX()
            if BinY > FR_Z.GetNbinsY():
                BinY = FR_Z.GetNbinsY()
            weight[0] = FR_Z.GetBinContent(BinX, BinY)/(1 - FR_Z.GetBinContent(BinX, BinY))
            number_of_loose += 1

        if event.z_lepton2_type == 0:
            BinX = FR_Z.GetXaxis().FindBin(abs(event.z_lepton2_eta))
            BinY = FR_Z.GetYaxis().FindBin(abs(event.z_lepton2_pt))
            # handle overflow
            if BinX > FR_Z.GetNbinsX():
                BinX = FR_Z.GetNbinsX()
            if BinY > FR_Z.GetNbinsY():
                BinY = FR_Z.GetNbinsY()
            weight[1] = FR_Z.GetBinContent(BinX, BinY)/(1 - FR_Z.GetBinContent(BinX, BinY)) 
            number_of_loose += 1

        if event.w_lepton_type == 0:
            BinX = FR_W.GetXaxis().FindBin(abs(event.w_lepton_eta))
            BinY = FR_W.GetYaxis().FindBin(abs(event.w_lepton_pt))
            # handle overflow
            if BinX > FR_W.GetNbinsX():
                BinX = FR_W.GetNbinsX()
            if BinY > FR_W.GetNbinsY():
                BinY = FR_W.GetNbinsY()
            weight[2] = FR_W.GetBinContent(BinX, BinY)/(1 - FR_W.GetBinContent(BinX, BinY)) 
            number_of_loose += 1
        
        fake_lepton_weight = weight[0]*weight[1]*weight[2]
        if number_of_loose == 2:
            fake_lepton_weight = -fake_lepton_weight

        self.out.fillBranch("fake_lepton_weight", fake_lepton_weight)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakeLeptonModule = lambda : ApplyWeightFakeLeptonProducer()