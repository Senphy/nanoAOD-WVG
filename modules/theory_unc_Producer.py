
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


class theory_unc_Producer(Module):
    def __init__(self):
        pass

    def _pdfWeight_cal(self, n, array):
        _weight = [1, 1, 1]
        if n==0 or n==1:
            return _weight
        rep = [x for x in range(0,n)]
        array = [array[x] for x in rep]
        rep.sort(key=lambda x: array[x])

        # e.g. n=100, down=16-1=15, up=84-1=83
        down = int(0.16 * n) - 1
        up = int(0.84 * n) - 1
        rep = rep[down:up+1]
        rep = [array[x] for x in rep]
        sigma = (rep[len(rep)-1] - rep[0])/2

        _weight[0] = sum(array) / n
        _weight[1] = _weight[0] + sigma
        _weight[2] = _weight[0] - sigma
        return _weight
        pass

    def _scaleWeight_cal(self, array):
        # Float_t LHE scale variation weights (w_var / w_nominal); [0] is MUF="0.5" MUR="0.5"; [1] is MUF="1.0" MUR="0.5"; [2] is MUF="2.0" MUR="0.5"; [3] is MUF="0.5" MUR="1.0"; [4] is MUF="1.0" MUR="1.0"; [5] is MUF="2.0" MUR="1.0"; [6] is MUF="0.5" MUR="2.0"; [7] is MUF="1.0" MUR="2.0"; [8] is MUF="2.0" MUR="2.0"*
        # Remove [6](0.5,2.0) and [2](2.0,0.5)
        rep = [x for x in range(0,9)]
        array = [array[x] for x in rep]
        _weight = [1, 1, 1]
        _weight[0] = array[4]
        array.pop(2)
        array.pop(6)
        _weight[1] = max(array)
        _weight[2] = min(array)
        return _weight
        pass

    def _psWeight_cal(self, array):
        rep = [x for x in range(0,4)]
        array = [array[x] for x in rep]
        _weight = [1, 1, 1]
        _weight[1] = max(array)
        _weight[2] = min(array)
        return _weight
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("pdf_Weight", "F")
        self.out.branch("pdf_WeightUp", "F")
        self.out.branch("pdf_WeightDown", "F")
        self.out.branch("scale_Weight", "F")
        self.out.branch("scale_WeightUp", "F")
        self.out.branch("scale_WeightDown", "F")
        self.out.branch("PS_Weight", "F")
        self.out.branch("PS_WeightUp", "F")
        self.out.branch("PS_WeightDown", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        pdf_Weight = self._pdfWeight_cal(event.nLHEPdfWeight, event.LHEPdfWeight)
        scale_Weight = self._scaleWeight_cal(event.LHEScaleWeight)
        PS_Weight = self._psWeight_cal(event.PSWeight)
        self.out.fillBranch("pdf_Weight", pdf_Weight[0])
        self.out.fillBranch("pdf_WeightUp", pdf_Weight[1])
        self.out.fillBranch("pdf_WeightDown", pdf_Weight[2])
        self.out.fillBranch("scale_Weight", scale_Weight[0])
        self.out.fillBranch("scale_WeightUp", scale_Weight[1])
        self.out.fillBranch("scale_WeightDown", scale_Weight[2])
        self.out.fillBranch("PS_Weight", PS_Weight[0])
        self.out.fillBranch("PS_WeightUp", PS_Weight[1])
        self.out.fillBranch("PS_WeightDown", PS_Weight[2])

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

theory_unc_Module = lambda : theory_unc_Producer()