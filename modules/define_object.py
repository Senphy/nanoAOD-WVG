
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


class define_object_Producer(Module):
    def __init__(self, year):
        self.year = year
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("nTightMuons", "i")
        self.out.branch("nTightElectrons", "i")
        self.out.branch("nTightPhotons", "i")
        self.out.branch("nJets", "i")
        self.out.branch("nbJets", "i")

        self.out.branch("nFakeMuons", "i")
        self.out.branch("nFakeElectrons", "i")
        self.out.branch("nFakePhotons", "i")
        
        self.out.branch("nVetoMuons", "i")
        self.out.branch("nVetoElectrons", "i")

        self.out.branch("TightMuons_index", "I", lenVar="nMuon")
        self.out.branch("TightElectrons_index", "I", lenVar="nElectron")
        self.out.branch("TightPhotons_index", "I", lenVar="nPhoton")
        self.out.branch("TightJets_index", "I", lenVar="nJet")
        self.out.branch("TightbJets_index", "I", lenVar="nJet")

        self.out.branch("FakeMuons_index", "I", lenVar="nMuon")
        self.out.branch("FakeElectrons_index", "I", lenVar="nElectron")
        self.out.branch("FakePhotons_index", "I", lenVar="nPhoton")

        self.out.branch("VetoMuons_index", "I", lenVar="nMuon")
        self.out.branch("VetoElectrons_index", "I", lenVar="nElectron")

        self.out.branch("Photon_ID_Weight", "F")
        self.out.branch("Photon_ID_Weight_UP", "F")
        self.out.branch("Photon_ID_Weight_DOWN", "F")
        self.out.branch("Muon_ID_Weight", "F")
        self.out.branch("Muon_ID_Weight_UP", "F")
        self.out.branch("Muon_ID_Weight_DOWN", "F")
        self.out.branch("Electron_ID_Weight", "F")
        self.out.branch("Electron_ID_Weight_UP", "F")
        self.out.branch("Electron_ID_Weight_DOWN", "F")
        self.out.branch("Electron_RECO_Weight", "F")
        self.out.branch("Electron_RECO_Weight_UP", "F")
        self.out.branch("Electron_RECO_Weight_DOWN", "F")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        jet_select = [] 
        dileptonp4 = ROOT.TLorentzVector()
        tight_photons = []
        tight_electrons = [] 
        tight_muons = [] 
        tight_jets = [] 
        tight_bjets = []
        veto_muons = []
        veto_electrons = []
        fake_muons = []
        fake_electrons = []
        fake_photons = []

        #selection on muons
        for i in range(0,len(muons)):
            if event.Muon_corrected_pt[i] < 15:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].tightId and muons[i].pfRelIso04_all < 0.4:
                fake_muons.append(i)
            elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
                veto_muons.append(i)
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())

        Muon_ID_Weight = 1
        Muon_ID_Weight_UP = 1
        Muon_ID_Weight_DOWN = 1
        if hasattr(event, "Muon_CutBased_TightID_SF"):
            for i in tight_muons:
                Muon_ID_Weight = Muon_ID_Weight * event.Muon_CutBased_TightID_SF[i]
                Muon_ID_Weight_UP = max(Muon_ID_Weight_UP * (event.Muon_CutBased_TightID_SF[i] + event.Muon_CutBased_TightID_SFerr[i]), Muon_ID_Weight_UP * (event.Muon_CutBased_TightID_SF[i] - event.Muon_CutBased_TightID_SFerr[i]))
                Muon_ID_Weight_DOWN = min(Muon_ID_Weight_DOWN * (event.Muon_CutBased_TightID_SF[i] + event.Muon_CutBased_TightID_SFerr[i]), Muon_ID_Weight_DOWN * (event.Muon_CutBased_TightID_SF[i] - event.Muon_CutBased_TightID_SFerr[i]))
            for i in fake_muons:
                Muon_ID_Weight = Muon_ID_Weight * event.Muon_CutBased_TightID_SF[i]
                Muon_ID_Weight_UP = max(Muon_ID_Weight_UP * (event.Muon_CutBased_TightID_SF[i] + event.Muon_CutBased_TightID_SFerr[i]), Muon_ID_Weight_UP * (event.Muon_CutBased_TightID_SF[i] - event.Muon_CutBased_TightID_SFerr[i]))
                Muon_ID_Weight_DOWN = min(Muon_ID_Weight_DOWN * (event.Muon_CutBased_TightID_SF[i] + event.Muon_CutBased_TightID_SFerr[i]), Muon_ID_Weight_DOWN * (event.Muon_CutBased_TightID_SF[i] - event.Muon_CutBased_TightID_SFerr[i]))
            for i in veto_muons:
                Muon_ID_Weight = Muon_ID_Weight * event.Muon_CutBased_LooseID_SF[i]
                Muon_ID_Weight_UP = max(Muon_ID_Weight_UP * (event.Muon_CutBased_LooseID_SF[i] + event.Muon_CutBased_LooseID_SFerr[i]), Muon_ID_Weight_UP * (event.Muon_CutBased_LooseID_SF[i] - event.Muon_CutBased_LooseID_SFerr[i]))
                Muon_ID_Weight_DOWN = min(Muon_ID_Weight_DOWN * (event.Muon_CutBased_LooseID_SF[i] + event.Muon_CutBased_LooseID_SFerr[i]), Muon_ID_Weight_DOWN * (event.Muon_CutBased_LooseID_SF[i] - event.Muon_CutBased_LooseID_SFerr[i]))


        # selection on electrons
        for i in range(0,len(electrons)):
            if electrons[i].pt < 15:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased == 1:
                    fake_electrons.append(i)
                elif electrons[i].cutBased > 1:
                    veto_electrons.append(i)

        Electron_ID_Weight = 1
        Electron_ID_Weight_UP = 1
        Electron_ID_Weight_DOWN = 1
        Electron_RECO_Weight = 1
        Electron_RECO_Weight_UP = 1
        Electron_RECO_Weight_DOWN = 1
        if hasattr(event, "Electron_RECO_SF"):
            for i in tight_electrons:
                Electron_ID_Weight = Electron_ID_Weight * event.Electron_CutBased_MediumID_SF[i]
                Electron_ID_Weight_UP = max(Electron_ID_Weight_UP * (event.Electron_CutBased_MediumID_SF[i] + event.Electron_CutBased_MediumID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_MediumID_SF[i] - event.Electron_CutBased_MediumID_SFerr[i]))
                Electron_ID_Weight_DOWN = min(Electron_ID_Weight_DOWN * (event.Electron_CutBased_MediumID_SF[i] + event.Electron_CutBased_MediumID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_MediumID_SF[i] - event.Electron_CutBased_MediumID_SFerr[i]))
                Electron_RECO_Weight = Electron_RECO_Weight * event.Electron_RECO_SF[i]
                Electron_RECO_Weight_UP = max(Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))
                Electron_RECO_Weight_DOWN = min(Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))
            for i in fake_electrons:
                Electron_ID_Weight = Electron_ID_Weight * event.Electron_CutBased_VetoID_SF[i]
                Electron_ID_Weight_UP = max(Electron_ID_Weight_UP * (event.Electron_CutBased_VetoID_SF[i] + event.Electron_CutBased_VetoID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_VetoID_SF[i] - event.Electron_CutBased_VetoID_SFerr[i]))
                Electron_ID_Weight_DOWN = min(Electron_ID_Weight_DOWN * (event.Electron_CutBased_VetoID_SF[i] + event.Electron_CutBased_VetoID_SFerr[i]), Electron_ID_Weight * (event.Electron_CutBased_VetoID_SF[i] - event.Electron_CutBased_VetoID_SFerr[i]))
                Electron_RECO_Weight = Electron_RECO_Weight * event.Electron_RECO_SF[i]
                Electron_RECO_Weight_UP = max(Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_UP * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))
                Electron_RECO_Weight_DOWN = min(Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] + event.Electron_RECO_SFerr[i]), Electron_RECO_Weight_DOWN * (event.Electron_RECO_SF[i] - event.Electron_RECO_SFerr[i]))

        selected_muons = tight_muons + fake_muons + veto_muons
        selected_electrons = tight_electrons + fake_electrons + veto_electrons
        # selection on photons, but not requirement on photon number in this module
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

            for j in range(0,len(selected_muons)):
                if deltaR(muons[selected_muons[j]].eta,muons[selected_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(selected_electrons)):
                if deltaR(electrons[selected_electrons[j]].eta,electrons[selected_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            if photons[i].cutBased >= 2:
                tight_photons.append(i)
                continue

            # MinPtCut,PhoSCEtaMultiRangeCut,PhoSingleTowerHadOverEmCut,PhoFull5x5SigmaIEtaIEtaCut,PhoAnyPFIsoWithEACut,PhoAnyPFIsoWithEAAndQuadScalingCut,PhoAnyPFIsoWithEACut
            mask_iso_sigmaietaieta = (1<<1) | (1<<3) | (1<<5) | (1<<11) | (1<<13) # remove charge iso and sigmaietaieta cut in medium id

            bitmap = photons[i].vidNestedWPBitmap & mask_iso_sigmaietaieta
            if (bitmap == mask_iso_sigmaietaieta):
                fake_photons.append(i)


        Photon_ID_Weight = 1
        Photon_ID_Weight_UP = 1
        Photon_ID_Weight_DOWN = 1
        if hasattr(event, "Photon_CutBased_MediumID_SF"):
            for i in tight_photons:
                Photon_ID_Weight = Photon_ID_Weight * event.Photon_CutBased_TightID_SF[i]
                Photon_ID_Weight_UP = max(Photon_ID_Weight_UP * (event.Photon_CutBased_TightID_SF[i] + event.Photon_CutBased_TightID_SFerr[i]), Photon_ID_Weight_UP * (event.Photon_CutBased_TightID_SF[i] - event.Photon_CutBased_TightID_SFerr[i]))
                Photon_ID_Weight_DOWN = min(Photon_ID_Weight_DOWN * (event.Photon_CutBased_TightID_SF[i] + event.Photon_CutBased_TightID_SFerr[i]), Photon_ID_Weight_DOWN * (event.Photon_CutBased_TightID_SF[i] - event.Photon_CutBased_TightID_SFerr[i]))

        for i in range(0,len(jets)): 

            if event.Jet_pt_nom[i] < 30:
                continue

            if abs(jets[i].eta) > 2.4:
                continue

            if not jets[i].jetId == 6:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_photons)):
                if deltaR(jets[i].eta,jets[i].phi,photons[tight_photons[j]].eta,photons[tight_photons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(selected_electrons)):
                if deltaR(jets[i].eta,jets[i].phi,electrons[selected_electrons[j]].eta,electrons[selected_electrons[j]].phi) < 0.5:
                    pass_lepton_dr_cut = False

            for j in range(0,len(selected_muons)):
                if deltaR(jets[i].eta,jets[i].phi,muons[selected_muons[j]].eta,muons[selected_muons[j]].phi) < 0.5:
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

            # c-jet tag is based on two-D cuts, medium DeepJet WP:
            # UL17 CvsL=btagDeepFlavCvL: 0.085, CvsB=btagDeepFlavCvB: 0.34
            # UL18 CvsL=btagDeepFlavCvL: 0.099, CvsB=btagDeepFlavCvB: 0.325
            # c-tag not available in NANOAOD yet

            tight_jets.append(i)

            if event.Jet_pt_nom[i] >= 30:
                if self.year == '2016Pre':
                    if jets[i].btagDeepB > 0.8819:
                        tight_bjets.append(i)
                elif self.year == '2016Post':
                    if jets[i].btagDeepB > 0.8767:
                        tight_bjets.append(i)
                elif self.year == '2017':
                    if jets[i].btagDeepB > 0.7738:
                        tight_bjets.append(i)
                elif self.year == '2018':
                    if jets[i].btagDeepB > 0.7665:
                        tight_bjets.append(i)

        self.out.fillBranch("nTightMuons", len(tight_muons))
        self.out.fillBranch("nTightElectrons", len(tight_electrons))
        self.out.fillBranch("nTightPhotons", len(tight_photons))
        self.out.fillBranch("nFakeMuons", len(fake_muons))
        self.out.fillBranch("nFakeElectrons", len(fake_electrons))
        self.out.fillBranch("nFakePhotons", len(fake_photons))
        self.out.fillBranch("nVetoMuons", len(veto_muons))
        self.out.fillBranch("nVetoElectrons", len(veto_electrons))
        self.out.fillBranch("nJets", len(tight_jets))
        self.out.fillBranch("nbJets", len(tight_bjets))

        # Re-order and fill -1 to keep arrays regular
        tight_muons.sort(key=lambda x: event.Muon_corrected_pt[x], reverse=True)
        tight_electrons.sort(key=lambda x: electrons[x].pt, reverse=True)
        tight_photons.sort(key=lambda x: photons[x].pt, reverse=True)

        tight_muons.extend(np.zeros(event.nMuon-len(tight_muons), int) - 1)
        tight_electrons.extend(np.zeros(event.nElectron-len(tight_electrons), int) - 1)
        tight_photons.extend(np.zeros(event.nPhoton-len(tight_photons), int) - 1)
        tight_jets.extend(np.zeros(event.nJet-len(tight_jets), int) - 1)
        tight_bjets.extend(np.zeros(event.nJet-len(tight_bjets), int) - 1)
        fake_muons.extend(np.zeros(event.nMuon-len(fake_muons), int) - 1)
        fake_electrons.extend(np.zeros(event.nElectron-len(fake_electrons), int) - 1)
        fake_photons.extend(np.zeros(event.nPhoton-len(fake_photons), int) - 1)
        veto_muons.extend(np.zeros(event.nMuon-len(veto_muons), int) - 1)
        veto_electrons.extend(np.zeros(event.nElectron-len(veto_electrons), int) - 1)

        self.out.fillBranch("TightMuons_index", tight_muons)
        self.out.fillBranch("TightElectrons_index", tight_electrons)
        self.out.fillBranch("TightPhotons_index", tight_photons)
        self.out.fillBranch("TightJets_index", tight_jets)
        self.out.fillBranch("TightbJets_index", tight_bjets)
        self.out.fillBranch("FakeMuons_index", fake_muons)
        self.out.fillBranch("FakeElectrons_index", fake_electrons)
        self.out.fillBranch("FakePhotons_index", fake_photons)
        self.out.fillBranch("VetoMuons_index", veto_muons)
        self.out.fillBranch("VetoElectrons_index", veto_electrons)

        self.out.fillBranch("Photon_ID_Weight", Photon_ID_Weight)
        self.out.fillBranch("Photon_ID_Weight_UP", Photon_ID_Weight_UP)
        self.out.fillBranch("Photon_ID_Weight_DOWN", Photon_ID_Weight_DOWN)
        self.out.fillBranch("Muon_ID_Weight", Muon_ID_Weight)
        self.out.fillBranch("Muon_ID_Weight_UP", Muon_ID_Weight_UP)
        self.out.fillBranch("Muon_ID_Weight_DOWN", Muon_ID_Weight_DOWN)
        self.out.fillBranch("Electron_ID_Weight", Electron_ID_Weight)
        self.out.fillBranch("Electron_ID_Weight_UP", Electron_ID_Weight_UP)
        self.out.fillBranch("Electron_ID_Weight_DOWN", Electron_ID_Weight_DOWN)
        self.out.fillBranch("Electron_RECO_Weight", Electron_RECO_Weight)
        self.out.fillBranch("Electron_RECO_Weight_UP", Electron_RECO_Weight_UP)
        self.out.fillBranch("Electron_RECO_Weight_DOWN", Electron_RECO_Weight_DOWN)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

define_object_Module_16Pre = lambda : define_object_Producer("2016Pre")
define_object_Module_16Post = lambda : define_object_Producer("2016Post")
define_object_Module_17 = lambda : define_object_Producer("2017")
define_object_Module_18 = lambda : define_object_Producer("2018")