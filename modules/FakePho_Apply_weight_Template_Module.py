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
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_photon_weight",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        weight = 1
        endcap_pt_map = {
            "20-50": 0.523,
            "50-Inf": 0.331
        }

        barrel_pt_map = {
            "20-30": 0.773,
            "30-50": 0.520,
            "50-80": 0.342,
            "80-120": 0.319,
            "120-Inf": 0.305
        }

        if abs(event.WZG_photon_eta) < 1.4442:
            if (event.WZG_photon_pt >= 20) and (event.WZG_photon_pt < 30):
                weight = barrel_pt_map["20-30"]
            elif (event.WZG_photon_pt >= 30) and (event.WZG_photon_pt < 50):
                weight = barrel_pt_map["30-50"]
            elif (event.WZG_photon_pt >= 50) and (event.WZG_photon_pt < 80):
                weight = barrel_pt_map["50-80"]
            elif (event.WZG_photon_pt >= 80) and (event.WZG_photon_pt < 120):
                weight = barrel_pt_map["80-120"]
            elif (event.WZG_photon_pt >= 120):
                weight = barrel_pt_map["120-Inf"]
        
        elif (abs(event.WZG_photon_eta) > 1.566) and (abs(event.WZG_photon_eta) < 2.5):
            if (event.WZG_photon_pt >= 20) and (event.WZG_photon_pt < 50):
                weight = endcap_pt_map["20-50"]
            elif (event.WZG_photon_pt >= 50):
                weight = endcap_pt_map["50-Inf"]

        self.out.fillBranch("fake_photon_weight", weight)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakePhotonModule = lambda : ApplyWeightFakePhotonProducer()