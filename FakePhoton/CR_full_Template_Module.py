
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


class CR_FakePhotonFullProducer(Module):
    def __init__(self, year):
        self.year = year
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MET",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("photon_genPartFlav",  "I")
        self.out.branch("photon_vidNestedWPBitmap", "L")
        self.out.branch("photon_sieie",  "F")
        self.out.branch("photon_pfRelIso03_all",  "F")
        self.out.branch("photon_pfRelIso03_chg",  "F")
        self.out.branch("dilepton_mass",  "F")
        self.out.branch("Generator_weight","F")

        # self.out.branch("max_CMVA","F")
        # self.out.branch("max_CSVV2","F")
        # self.out.branch("max_DeepB","F")
        self.out.branch("channel_mark","i")
        self.out.branch("nJets","i")
        self.out.branch("nbJets","i")

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
        loose_but_not_tight_muons = []
        loose_but_not_tight_electrons = []
        tight_without_iso_sigmaietaieta_photons = []

        # selection on MET. Pass to next event directly if fail.
        if hasattr(event, "MET_T1Smear_pt"):
            self.out.fillBranch("MET",event.MET_T1Smear_pt)
        else:
            self.out.fillBranch("MET",event.MET_pt)


        #selection on muons
        for i in range(0,len(muons)):
            if muons[i].pt < 15:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
                loose_but_not_tight_muons.append(i)


        # selection on electrons
        for i in range(0,len(electrons)):
            if electrons[i].pt < 15:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        # speed up
        if len(tight_electrons)+len(tight_muons) < 2:
            return False
        elif len(tight_electrons)+len(tight_muons) > 3:
            return False
        if len(loose_but_not_tight_electrons) + len(loose_but_not_tight_muons) > 0:
            return False

        # selection on photons, but not requirement on photon number in this module
        for i in range(0,len(photons)):

            # This condition should be changed for different process
            #  photons[i].genPartFlav == 1:
                # continue
            
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

            # MinPtCut,PhoSCEtaMultiRangeCut,PhoSingleTowerHadOverEmCut,PhoFull5x5SigmaIEtaIEtaCut,PhoAnyPFIsoWithEACut,PhoAnyPFIsoWithEAAndQuadScalingCut,PhoAnyPFIsoWithEACut
            mask_full = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11) | (1<<13) 
            mask_iso_sigmaietaieta = (1<<1) | (1<<3) | (1<<5) | (1<<11) | (1<<13) # remove charge iso and sigmaietaieta cut in medium id

            bitmap = photons[i].vidNestedWPBitmap & mask_iso_sigmaietaieta
            if (bitmap == mask_iso_sigmaietaieta):
                tight_without_iso_sigmaietaieta_photons.append(i)

            bitmap = photons[i].vidNestedWPBitmap & mask_full
            if (bitmap == mask_full):
                tight_photons.append(i)

        if len(tight_photons) + len(tight_without_iso_sigmaietaieta_photons) == 0:
            return False


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

            # c-jet tag is based on two-D cuts, medium DeepJet WP:
            # UL17 CvsL=btagDeepFlavCvL: 0.085, CvsB=btagDeepFlavCvB: 0.34
            # UL18 CvsL=btagDeepFlavCvL: 0.099, CvsB=btagDeepFlavCvB: 0.325
            # c-tag not available in NANOAOD yet

            tight_jets.append(i)

            if event.Jet_pt_nom[i] >= 30:
                if self.year == '2017':
                    if jets[i].btagDeepB > 0.7738:
                            tight_bjets.append(i)
                elif self.year == '2018':
                    if jets[i].btagDeepB > 0.7665:
                            tight_bjets.append(i)

        self.out.fillBranch("nJets", len(tight_jets))
        self.out.fillBranch("nbJets", len(tight_bjets))

        #dilepton mass selection and channel selection
        channel = 0 
        # emumu:     1
        # muee:      2
        # eee:       3 
        # mumumu:    4 
        # ee         31
        # mumu       32

        if len(tight_electrons)+len(tight_muons) == 2:
            if len(tight_electrons) == 2:
                dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
                channel = 31
            elif len(tight_muons) == 2:
                dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                channel = 32
            else:
                return False
            
            if dileptonmass < 4 or abs(dileptonmass-91.188) > 15:
                return False

            self.out.fillBranch("photon_pt",photons[tight_without_iso_sigmaietaieta_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_without_iso_sigmaietaieta_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_without_iso_sigmaietaieta_photons[0]].phi)
            self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_without_iso_sigmaietaieta_photons[0]].vidNestedWPBitmap)
            self.out.fillBranch("photon_sieie",photons[tight_without_iso_sigmaietaieta_photons[0]].sieie)
            self.out.fillBranch("photon_pfRelIso03_all",photons[tight_without_iso_sigmaietaieta_photons[0]].pfRelIso03_all)
            self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_without_iso_sigmaietaieta_photons[0]].pfRelIso03_chg)
            if hasattr(photons[tight_without_iso_sigmaietaieta_photons[0]], "genPartFlav"):
                self.out.fillBranch("photon_genPartFlav",photons[tight_without_iso_sigmaietaieta_photons[0]].genPartFlav)
            else:
                self.out.fillBranch("photon_genPartFlav",-1)

            if hasattr(event, "Generator_weight"):
                self.out.fillBranch("Generator_weight",event.Generator_weight)
            else:
                self.out.fillBranch("Generator_weight",0)
            self.out.fillBranch("channel_mark",channel)
            self.out.fillBranch("dilepton_mass",dileptonmass)
            return True

        elif len(tight_electrons)+len(tight_muons) == 3:
            # emumu
            dileptonmass = -1.0
            if len(tight_muons)==2 and len(tight_electrons)==1:  # emumu channel 
                if muons[tight_muons[0]].pdgId == -muons[tight_muons[1]].pdgId:
                    if (muons[tight_muons[0]].pt >= 25) and (electrons[tight_electrons[0]].pt >= 25):
                        dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                        channel = 1
                
            # muee
            if len(tight_muons)==1 and len(tight_electrons)==2:
                if electrons[tight_electrons[0]].pdgId == -electrons[tight_electrons[1]].pdgId:
                    if (muons[tight_muons[0]].pt >= 25) and (electrons[tight_electrons[0]].pt >= 25):
                        dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
                        channel = 2

            # eee 
            if len(tight_electrons)==3 and len(tight_muons)==0:
                # move the different charge lepton to the end for further analysis
                if (electrons[tight_electrons[0]].charge == electrons[tight_electrons[1]].charge) and (electrons[tight_electrons[0]].charge == electrons[tight_electrons[2]].charge):
                    pass # reject events for +++/---
                else:
                    if electrons[tight_electrons[0]].charge == electrons[tight_electrons[2]].charge:
                        tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1] # e.g. +-+ -> ++-
                    elif electrons[tight_electrons[1]].charge == electrons[tight_electrons[2]].charge:
                        tight_electrons[0],tight_electrons[2] = tight_electrons[2],tight_electrons[0] # e.g. -++ -> ++-
                
                    # compute mll and compare to mz, leptons with cloest mll to mz are considered to be z_leptons. Remaining lepton is w_lepton.
                    mll13 = -1.0
                    mll23 = -1.0
                    mll13 = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[2]].p4()).M()
                    mll23 = (electrons[tight_electrons[1]].p4() + electrons[tight_electrons[2]].p4()).M()
                    if abs(mll13 - 91.188) > abs(mll23 - 91.188):
                        dileptonmass = mll23
                    else:
                        tight_electrons[0],tight_electrons[1] = tight_electrons[1],tight_electrons[0] # move the w_lepton to the first one
                        dileptonmass = mll13

                    if electrons[tight_electrons[1]].pt < electrons[tight_electrons[2]].pt:
                        tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1]
                    
                    if (electrons[tight_electrons[0]].pt >= 25) and (electrons[tight_electrons[1]].pt >= 25):
                        channel = 3


            # mumumu
            if len(tight_muons)==3 and len(tight_electrons)==0:
                # move the different charge lepton to the end for further analysis
                if (muons[tight_muons[0]].charge == muons[tight_muons[1]].charge) and (muons[tight_muons[0]].charge == muons[tight_muons[2]].charge):
                    pass
                else:
                    if muons[tight_muons[0]].charge == muons[tight_muons[2]].charge:
                        tight_muons[1],tight_muons[2] = tight_muons[2],tight_muons[1] # e.g. +-+ -> ++-
                    elif muons[tight_muons[1]].charge == muons[tight_muons[2]].charge:
                        tight_muons[0],tight_muons[2] = tight_muons[2],tight_muons[0] # e.g. -++ -> ++-
                
                    # compute mll and compare to mz, leptons with cloest mll to mz are considered to be z_leptons. Remaining lepton is w_lepton.
                    mll13 = -1.0
                    mll23 = -1.0
                    mll13 = (muons[tight_muons[0]].p4() + muons[tight_muons[2]].p4()).M()
                    mll23 = (muons[tight_muons[1]].p4() + muons[tight_muons[2]].p4()).M()
                    if abs(mll13 - 91.188) > abs(mll23 - 91.188):
                        dileptonmass = mll23
                    else:
                        tight_muons[0],tight_muons[1] = tight_muons[1],tight_muons[0] # move the w_lepton to the first one
                        dileptonmass = mll13

                    if muons[tight_muons[1]].pt < muons[tight_muons[2]].pt:
                        tight_muons[1],tight_muons[2] = tight_muons[2], tight_muons[1]
                    
                    if (muons[tight_muons[0]].pt >= 25) and (muons[tight_muons[1]].pt >= 25):
                        channel = 4

            if dileptonmass < 4 or abs(dileptonmass-91.188) > 15:
                return False

            if channel == 0:
                return False

            self.out.fillBranch("photon_pt",photons[tight_without_iso_sigmaietaieta_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_without_iso_sigmaietaieta_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_without_iso_sigmaietaieta_photons[0]].phi)
            self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_without_iso_sigmaietaieta_photons[0]].vidNestedWPBitmap)
            self.out.fillBranch("photon_sieie",photons[tight_without_iso_sigmaietaieta_photons[0]].sieie)
            self.out.fillBranch("photon_pfRelIso03_all",photons[tight_without_iso_sigmaietaieta_photons[0]].pfRelIso03_all)
            self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_without_iso_sigmaietaieta_photons[0]].pfRelIso03_chg)
            if hasattr(photons[tight_without_iso_sigmaietaieta_photons[0]], "genPartFlav"):
                self.out.fillBranch("photon_genPartFlav",photons[tight_without_iso_sigmaietaieta_photons[0]].genPartFlav)
            else:
                self.out.fillBranch("photon_genPartFlav",-1)

            if hasattr(event, "Generator_weight"):
                self.out.fillBranch("Generator_weight",event.Generator_weight)
            else:
                self.out.fillBranch("Generator_weight",0)
            self.out.fillBranch("channel_mark",channel)
            self.out.fillBranch("dilepton_mass",dileptonmass)

            return True

class first_Template_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nLooseNotTightLep","I")
        self.out.branch("nTightLep","I")
        self.out.branch("nTightMuon","I")
        self.out.branch("nTightElectron","I")
        self.out.branch("nLooseNotTightMuon","I")
        self.out.branch("nLooseNotTightElectron","I")
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        # photons = Collection(event, "Photon")
        tight_electrons = [] 
        tight_muons = [] 
        veto_muons = []
        veto_electrons = []

        if (event.nElectron + event.nMuon) < 2:
            return False

        for i in range(0,len(muons)):
            if muons[i].pt < 15:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].looseId and muons[i].pfRelIso04_all < 0.4:
                veto_muons.append(i)

        # selection on electrons
        for i in range(0,len(electrons)):
            if electrons[i].pt < 15:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased >= 1:
                    veto_electrons.append(i)

        if len(veto_electrons)+len(veto_muons) != 0:
            return False

        if (len(tight_electrons) + len(tight_muons) > 3) or (len(tight_electrons) + len(tight_muons) < 2):
            return False
        
        self.out.fillBranch("nLooseNotTightLep", len(veto_muons)+len(veto_electrons))
        self.out.fillBranch("nTightLep", len(tight_muons)+len(tight_electrons))
        self.out.fillBranch("nTightMuon", len(tight_muons))
        self.out.fillBranch("nTightElectron", len(tight_electrons))
        self.out.fillBranch("nLooseNotTightMuon", len(veto_muons))
        self.out.fillBranch("nLooseNotTightElectron", len(veto_electrons))

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

CR_FakePhotonFullModule_18 = lambda : CR_FakePhotonFullProducer("2018")
CR_FakePhotonFullModule_17 = lambda : CR_FakePhotonFullProducer("2017")
first_Template_Module = lambda : first_Template_Producer()