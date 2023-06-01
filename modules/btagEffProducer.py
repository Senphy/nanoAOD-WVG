import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import math
import os

class btagEffProducer(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_btag_bjet = ROOT.TH2D('h_btag_bjet', 'h_btag_bjet', 10, 0, 300, 6, -2.4, 2.4)
        self.h_btag_cjet = ROOT.TH2D('h_btag_cjet', 'h_btag_cjet', 10, 0, 300, 6, -2.4, 2.4)
        self.h_btag_ljet = ROOT.TH2D('h_btag_ljet', 'h_btag_ljet', 10, 0, 300, 6, -2.4, 2.4)
        self.h_bjet = ROOT.TH2D('h_bjet', 'h_bjet', 10, 0, 300, 6, -2.4, 2.4)
        self.h_cjet = ROOT.TH2D('h_cjet', 'h_cjet', 10, 0, 300, 6, -2.4, 2.4)
        self.h_ljet = ROOT.TH2D('h_ljet', 'h_ljet', 10, 0, 300, 6, -2.4, 2.4)
        self.out = wrappedOutputTree
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_btag_bjet.Write()
        self.h_btag_cjet.Write()
        self.h_btag_ljet.Write()
        self.h_bjet.Write()
        self.h_cjet.Write()
        self.h_ljet.Write()
        prevdir.cd()
        pass

    def analyze(self, event):
        jets = Collection(event, "Jet")
        tight_jets = event.TightJets_index[:event.nJets]
        tight_bjets = event.TightbJets_index[:event.nbJets]

        for i in tight_bjets:
            if jets[i].hadronFlavour == 5:
                self.h_btag_bjet.Fill(jets[i].pt, jets[i].eta, math.copysign(1, event.Generator_weight))
            elif jets[i].hadronFlavour == 4:
                self.h_btag_cjet.Fill(jets[i].pt, jets[i].eta, math.copysign(1, event.Generator_weight))
            elif jets[i].hadronFlavour == 0:
                self.h_btag_ljet.Fill(jets[i].pt, jets[i].eta, math.copysign(1, event.Generator_weight))

        for i in tight_jets:
            if jets[i].hadronFlavour == 5:
                self.h_bjet.Fill(jets[i].pt, jets[i].eta, math.copysign(1, event.Generator_weight))
            elif jets[i].hadronFlavour == 4:
                self.h_cjet.Fill(jets[i].pt, jets[i].eta, math.copysign(1, event.Generator_weight))
            elif jets[i].hadronFlavour == 0:
                self.h_ljet.Fill(jets[i].pt, jets[i].eta, math.copysign(1, event.Generator_weight))
        
        return True

btagEffModule = lambda: btagEffProducer()
