#!/usr/bin/env python
# Refer to 1d) method from https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1d_Event_reweighting_using_discr
# details: https://twiki.cern.ch/twiki/bin/view/CMS/BTagShapeCalibration
# Need to process after btv official module: https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/btv/btagSFProducer.py
# Also refer to Latino framework: https://github.com/latinos/LatinoAnalysis/blob/master/NanoGardener/python/modules/BTagEventWeightProducer.py
# Noticed that this module should performed before the b tag cut and measure the sum of event weights before and after applying b-tag event weights.

import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class btagWeightProduce(Module):
    def __init__(self, year):
        self.year = year
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MET",  "F")
        self.systs_shape_corr = []
        for syst in [ 'jes',
                      'lf', 'hf',
                      'hfstats1', 'hfstats2',
                      'lfstats1', 'lfstats2',
                      'cferr1', 'cferr2' ]:
            self.systs_shape_corr.append("up_%s" % syst)
            self.systs_shape_corr.append("down_%s" % syst)
            self.central_and_systs_shape_corr = [ "central" ]
            self.central_and_systs_shape_corr.extend(self.systs_shape_corr)
            self.branchNames_central_and_systs_shape_corr={}
            for central_or_syst in self.central_and_systs_shape_corr:
                if central_or_syst == "central":
                    self.branchNames_central_and_systs_shape_corr[central_or_syst] = "btagWeight"
                else:
                    self.branchNames_central_and_systs_shape_corr[central_or_syst] = "btagWeight_%s" % central_or_syst
                self.out.branch(self.branchNames_central_and_systs_shape_corr[central_or_syst],'F')     

        self.h_neventsgenweighted_btag = ROOT.TH1D('h_nEventsGenWeighted_btag','h_nEventsGenWeighted_btag', 1, 0, 1)
        self.h_neventsgenweighted = ROOT.TH1D('h_nEventsGenWeighted','h_nEventsGenWeighted', 1, 0, 1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        # self.h_nevents.Write()
        #        self.h_nweightedevents.Write()
        self.h_neventsgenweighted_btag.Write()
        self.h_neventsgenweighted.Write()
        self.h_neventsgenweighted_ratio = self.h_neventsgenweighted.Clone("h_nEventsGenWeighted_ratio")
        self.h_neventsgenweighted_ratio.Divide(self.h_neventsgenweighted_btag)
        self.h_neventsgenweighted_ratio.Write()
        prevdir.cd()
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        tight_muons = []
        tight_electrons = []
        tight_photons = []
        tight_jets = []
        tight_bjets = []
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")

        for i in range(0,len(muons)):
            if event.Muon_corrected_pt[i] < 10:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())

        for i in range(0,len(electrons)):
            if electrons[i].pt < 10:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
                continue
            if photons[i].pixelSeed:
                continue
            pass_lepton_dr_cut = True
            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(tight_electrons)):
                if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue
            if photons[i].cutBased < 2:
                continue
            tight_photons.append(i)


        for i in range(0,len(jets)): 
            if event.Jet_pt_nom[i] < 10:
                continue
            if abs(jets[i].eta) > 2.4:
                continue
            if not jets[i].jetId == 6:
                continue
            pass_lepton_dr_cut = True
            for j in range(0,len(tight_photons)):
                if deltaR(jets[i].eta,jets[i].phi,photons[tight_photons[j]].eta,photons[tight_photons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(tight_electrons)):
                if deltaR(jets[i].eta,jets[i].phi,electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(tight_muons)):
                if deltaR(jets[i].eta,jets[i].phi,muons[tight_muons[j]].eta,muons[tight_muons[j]].phi) < 0.5:
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

            tight_jets.append(i)

            if event.Jet_pt_nom[i] >= 30:
                if self.year == '2017':
                    if jets[i].btagDeepB > 0.7738:
                        tight_bjets.append(i)
                elif self.year == '2018':
                    if jets[i].btagDeepB > 0.7665:
                        tight_bjets.append(i)
        

        btag_weight = 1.
        for central_or_syst in self.central_and_systs_shape_corr:
            btag_weight = 1.
            if central_or_syst == "central":
                for idx in tight_bjets:
                    btag_weight *= event.Jet_btagSF_deepcsv_shape[idx]
                    # print(type(btag_weight))
                    # print(btag_weight)
            else:
                for idx in tight_bjets:
                    btag_weight *= getattr(event, "Jet_btagSF_deepcsv_shape_%s" %central_or_syst)[idx]
            # print btag_weight
            self.out.fillBranch(self.branchNames_central_and_systs_shape_corr[central_or_syst], btag_weight)

        if hasattr(event, 'Generator_weight') and event.Generator_weight < 0:
            self.h_neventsgenweighted_btag.Fill(len(tight_jets), -1 * btag_weight)
            self.h_neventsgenweighted.Fill(len(tight_jets), -1)
        else:
            self.h_neventsgenweighted_btag.Fill(len(tight_jets), 1 * btag_weight)
            self.h_neventsgenweighted.Fill(len(tight_jets), 1)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

btagWeightModule_16 = lambda : btagWeightProduce("2016")
btagWeightModule_17 = lambda : btagWeightProduce("2017")
btagWeightModule_18 = lambda : btagWeightProduce("2018")