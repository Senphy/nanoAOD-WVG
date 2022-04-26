
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


class FakePho_test_Producer(Module):
    def __init__(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("ZGJ_photon_vidNestedWPBitmap",  "L")
        self.out.branch("ZGJ_photon_pfRelIso03_chg", "F")
        self.out.branch("ZGJ_photon_sieie", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        photons = Collection(event, "Photon")

        if event.channel_mark in [31,32]:

        # 31: ZGJets_ee
        # 32: ZGJets_mm

            self.out.fillBranch("ZGJ_photon_vidNestedWPBitmap", photons[event.ZGJ_photon_index].vidNestedWPBitmap)
            self.out.fillBranch("ZGJ_photon_pfRelIso03_chg", photons[event.ZGJ_photon_index].pfRelIso03_chg)
            self.out.fillBranch("ZGJ_photon_sieie", photons[event.ZGJ_photon_index].sieie)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

FakePho_test_Module = lambda : FakePho_test_Producer()