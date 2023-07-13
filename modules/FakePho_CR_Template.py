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


class FakePho_CR_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MET",  "F")
        self.out.branch("photon_type",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("photon_genPartFlav",  "I")
        self.out.branch("photon_vidNestedWPBitmap", "L")
        self.out.branch("photon_sieie",  "F")
        self.out.branch("photon_pfRelIso03_all",  "F")
        self.out.branch("photon_pfRelIso03_chg",  "F")
        self.out.branch("mll",  "F")
        self.out.branch("Generator_weight","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        tight_photons = []
        tight_without_chgiso_sieie_photons = []
        tight_without_iso_sieie_photons = []

        # selection on MET. Pass to next event directly if fail.
        if hasattr(event, "MET_T1Smear_pt"):
            MET = event.MET_T1Smear_pt
            self.out.fillBranch("MET",event.MET_T1Smear_pt)
        else:
            MET = event.MET_pt
            self.out.fillBranch("MET",event.MET_pt)
        
        # For speed up
        if (event.nTightMuons + event.nTightElectrons) != 2:
            return False
        if (event.nFakeMuons + event.nFakeElectrons + event.nVetoMuons + event.nVetoElectrons) > 0:
            return False
        
        # Load Objects
        # *FIXME* Potential bugs here for TTreeArray conversion.
        # Can't run seperately without define_object module
        tight_muons = event.TightMuons_index[:event.nTightMuons]
        for i in tight_muons:
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())
        tight_electrons = event.TightElectrons_index[:event.nTightElectrons]

        if event.nTightMuons == 2:
            if muons[tight_muons[0]].charge != -muons[tight_muons[1]].charge:
                return False
            else:
                mll = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
        if event.nTightElectrons == 2:
            if electrons[tight_electrons[0]].charge != -electrons[tight_electrons[1]].charge:
                return False
            else:
                mll = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
        else:
            return False
        
        if mll < 4 or abs(mll-91.188) > 15:
            return False

        # selection on photons, but not requirement on photon number in this module
        # re-id photon for template fit CR
        for i in range(0,len(photons)):

            # This condition should be changed for different process
            #  photons[i].genPartFlav == 1:
                # continue
            
            if photons[i].pt < 15:
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

            # MinPtCut,PhoSCEtaMultiRangeCut,PhoSingleTowerHadOverEmCut,PhoFull5x5SigmaIEtaIEtaCut,ChHadIsoWithEALinScalingCut,NeuHadIsoWithEAQuadScalingCut,PhoIsoWithEALinScalingCut
            mask_full = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11) | (1<<13) 

            # remove chgiso sieie
            mask_chgiso_sieie = (1<<1) | (1<<3) | (1<<5) | (1<<11) | (1<<13)
            # remove iso sieie
            mask_iso_sieie = (1<<1) | (1<<3) | (1<<5)

            # # remove sieie 
            # mask_sieie = (1<<1) | (1<<3) | (1<<5) | (1<<9) | (1<<11) | (1<<13)
            # # remove charge iso
            # mask_chgiso = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<11) | (1<<13)
            # # remove neutral iso
            # mask_neuiso = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<13)
            # # remove pho iso
            # mask_phoiso = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11)

            bitmap = photons[i].vidNestedWPBitmap & mask_iso_sieie
            if (bitmap == mask_iso_sieie):
                tight_without_iso_sieie_photons.append(i)

            bitmap = photons[i].vidNestedWPBitmap & mask_chgiso_sieie
            if (bitmap == mask_chgiso_sieie):
                tight_without_chgiso_sieie_photons.append(i)

            bitmap = photons[i].vidNestedWPBitmap & mask_full
            if (bitmap == mask_full):
                tight_photons.append(i)

        if len(tight_photons) + len(tight_without_chgiso_sieie_photons) + len(tight_without_iso_sieie_photons) == 0:
            return False
        
        # photon_type 1:tight_without_iso_sieie 2:tight_without_chgiso_sieie 3:tight
        photon_type = 1
        if tight_without_iso_sieie_photons[0] in tight_photons:
            photon_type = 3
        elif tight_without_iso_sieie_photons[0] in tight_without_chgiso_sieie_photons:
            photon_type = 2
        else:
            photon_type = 1

        self.out.fillBranch("photon_type",photon_type)
        self.out.fillBranch("photon_pt",photons[tight_without_iso_sieie_photons[0]].pt)
        self.out.fillBranch("photon_eta",photons[tight_without_iso_sieie_photons[0]].eta)
        self.out.fillBranch("photon_phi",photons[tight_without_iso_sieie_photons[0]].phi)
        self.out.fillBranch("photon_vidNestedWPBitmap",photons[tight_without_iso_sieie_photons[0]].vidNestedWPBitmap)
        self.out.fillBranch("photon_sieie",photons[tight_without_iso_sieie_photons[0]].sieie)
        self.out.fillBranch("photon_pfRelIso03_all",photons[tight_without_iso_sieie_photons[0]].pfRelIso03_all)
        self.out.fillBranch("photon_pfRelIso03_chg",photons[tight_without_iso_sieie_photons[0]].pfRelIso03_chg)
        if hasattr(photons[tight_without_iso_sieie_photons[0]], "genPartFlav"):
            self.out.fillBranch("photon_genPartFlav",photons[tight_without_iso_sieie_photons[0]].genPartFlav)
        else:
            self.out.fillBranch("photon_genPartFlav",-1)

        if hasattr(event, "Generator_weight"):
            self.out.fillBranch("Generator_weight",event.Generator_weight)
        else:
            self.out.fillBranch("Generator_weight",0)
        self.out.fillBranch("mll",mll)
        
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

FakePho_CR_Module = lambda : FakePho_CR_Producer()