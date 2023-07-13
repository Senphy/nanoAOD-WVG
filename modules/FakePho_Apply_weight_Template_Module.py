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

        self.endcap_pt_map = {
            "2018":{
                "ptbins":[15, 50, 5000],
                "weight":[0.166, 0.092],
                "unc":[0.004, 0.009],
            }
        }

        self.barrel_pt_map = {
            "2018":{
                "ptbins":[15, 20, 30, 50, 80, 120, 5000],
                "weight":[0.188, 0.149, 0.099, 0.075, 0.069, 0.117],
                "unc":[0.002, 0.003, 0.002, 0.004, 0.005, 0.200],
            }
        }


    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_photon_weight",  "F")
        self.out.branch("fake_photon_weight_statup",  "F")
        self.out.branch("fake_photon_weight_statdown",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def calweight(self, pt, eta):
        weight = 1
        if abs(eta) < 1.4442:
            for i in range(0, len(self.barrel_pt_map[self.year]['ptbins'])-1):
                pt_low = self.barrel_pt_map[self.year]['ptbins'][i]
                pt_high = self.barrel_pt_map[self.year]['ptbins'][i+1]
                if (pt >= pt_low) and (pt <= pt_high):
                    weight = self.barrel_pt_map[self.year]['weight'][i]
                    weight_up = self.barrel_pt_map[self.year]['weight'][i] + self.barrel_pt_map[self.year]['unc'][i]
                    weight_down = max(self.barrel_pt_map[self.year]['weight'][i] - self.barrel_pt_map[self.year]['unc'][i], 0)

        elif (abs(eta) > 1.566) and (abs(eta) < 2.5):
            for i in range(0, len(self.endcap_pt_map[self.year]['ptbins'])-1):
                pt_low = self.endcap_pt_map[self.year]['ptbins'][i]
                pt_high = self.endcap_pt_map[self.year]['ptbins'][i+1]
                if (pt >= pt_low) and (pt <= pt_high):
                    weight = self.endcap_pt_map[self.year]['weight'][i]
                    weight_up = self.endcap_pt_map[self.year]['weight'][i] + self.endcap_pt_map[self.year]['unc'][i]
                    weight_down = max(self.endcap_pt_map[self.year]['weight'][i] - self.endcap_pt_map[self.year]['unc'][i], 0)

        return weight, weight_up, weight_down

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        weight,weight_up,weight_down = 1,1,1
        if event.region_mark == 3:
            if event.channel_mark in [1,2,3,4]:
                weight,weight_up,weight_down = self.calweight(event.WZG_photon_pt, event.WZG_photon_eta) 
            elif event.channel_mark in [31,32]:
                weight,weight_up,weight_down = self.calweight(event.ZGJ_photon_pt, event.ZGJ_photon_eta) 
            elif event.channel_mark in [21,22,23,24]:
                weight,weight_up,weight_down = self.calweight(event.ttG_photon_pt, event.ttG_photon_eta) 

        self.out.fillBranch("fake_photon_weight", weight)
        self.out.fillBranch("fake_photon_weight_statup", weight_up)
        self.out.fillBranch("fake_photon_weight_statdown", weight_down)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakePhotonModule = lambda : ApplyWeightFakePhotonProducer()
ApplyWeightFakePhotonModule18 = lambda : ApplyWeightFakePhotonProducer('2018')
ApplyWeightFakePhotonModule17 = lambda : ApplyWeightFakePhotonProducer('2017')
ApplyWeightFakePhotonModule16 = lambda : ApplyWeightFakePhotonProducer('2016')