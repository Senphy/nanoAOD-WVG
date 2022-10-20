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



class ApplyWeightFakePhotonProducer(Module):
    def __init__(self, year):
        pass
        self.year = year

        self.endcap_pt_map_16 = {
            "20-50": 0.300,
            "50-Inf": 0.220
        }

        self.barrel_pt_map_16 = {
            "20-30": 0.390,
            "30-50": 0.280,
            "50-80": 0.200,
            "80-120": 0.140,
            "120-Inf": 0.120
        }

        self.endcap_pt_map_17 = {
            "20-50": 0.239,
            "50-Inf": 0.183
        }

        self.barrel_pt_map_17 = {
            "20-30": 0.337,
            "30-50": 0.255,
            "50-80": 0.182,
            "80-120": 0.144,
            "120-Inf": 0.128
        }

        self.endcap_pt_map_18 = {
            "20-50": 0.204,
            "50-Inf": 0.122
        }

        self.barrel_pt_map_18 = {
            "20-30": 0.297,
            "30-50": 0.205,
            "50-80": 0.145,
            "80-120": 0.123,
            "120-Inf": 0.085
        }

        if str(self.year) == '2018':
            self.endcap_pt_map = self.endcap_pt_map_18
            self.barrel_pt_map = self.barrel_pt_map_18
        elif str(self.year) == '2017':
            self.endcap_pt_map = self.endcap_pt_map_17
            self.barrel_pt_map = self.barrel_pt_map_17
        elif str(self.year) == '2016':
            self.endcap_pt_map = self.endcap_pt_map_16
            self.barrel_pt_map = self.barrel_pt_map_16
        

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_photon_weight",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def calweight(self, pt, eta):
        weight = 1
        if abs(eta) < 1.4442:
            if (pt >= 20) and (pt < 30):
                weight = self.barrel_pt_map["20-30"]
            elif (pt >= 30) and (pt < 50):
                weight = self.barrel_pt_map["30-50"]
            elif (pt >= 50) and (pt < 80):
                weight = self.barrel_pt_map["50-80"]
            elif (pt >= 80) and (pt < 120):
                weight = self.barrel_pt_map["80-120"]
            elif (pt >= 120):
                weight = self.barrel_pt_map["120-Inf"]
        
        elif (abs(eta) > 1.566) and (abs(eta) < 2.5):
            if (pt >= 20) and (pt < 50):
                weight = self.endcap_pt_map["20-50"]
            elif (pt >= 50):
                weight = self.endcap_pt_map["50-Inf"]

        return weight

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        weight = 1
        if event.region_mark == 3:
            if event.channel_mark in [1,2,3,4]:
                weight = self.calweight(event.WZG_photon_pt, event.WZG_photon_eta) 
            elif event.channel_mark in [31,32]:
                weight = self.calweight(event.ZGJ_photon_pt, event.ZGJ_photon_eta) 
            elif event.channel_mark in [21,22,23,24]:
                weight = self.calweight(event.ttG_photon_pt, event.ttG_photon_eta) 

        self.out.fillBranch("fake_photon_weight", weight)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakePhotonModule = lambda : ApplyWeightFakePhotonProducer()
ApplyWeightFakePhotonModule18 = lambda : ApplyWeightFakePhotonProducer('2018')
ApplyWeightFakePhotonModule17 = lambda : ApplyWeightFakePhotonProducer('2017')
ApplyWeightFakePhotonModule16 = lambda : ApplyWeightFakePhotonProducer('2016')