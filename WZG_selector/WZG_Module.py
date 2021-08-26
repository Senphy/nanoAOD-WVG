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


class WZG_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MET",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("photon_genPartFlav",  "I")
        self.out.branch("photon_mark",  "I")
        self.out.branch("z_lepton1_genPartFlav",  "I")
        self.out.branch("z_lepton2_genPartFlav",  "I")
        self.out.branch("w_lepton_genPartFlav",  "I")
        self.out.branch("z_lepton1_pt",  "F")
        self.out.branch("z_lepton1_eta",  "F")
        self.out.branch("z_lepton1_phi",  "F")
        self.out.branch("z_lepton2_pt",  "F")
        self.out.branch("z_lepton2_eta",  "F")
        self.out.branch("z_lepton2_phi",  "F")
        self.out.branch("w_lepton_pt",  "F")
        self.out.branch("w_lepton_eta",  "F")
        self.out.branch("w_lepton_phi",  "F")
        self.out.branch("dilepton_mass",  "F")
        self.out.branch("Generator_weight","F")
        self.out.branch("More_than_three_tight_lep","I")
        self.out.branch("have_loose_lep","I")
        # self.out.branch("max_CMVA","F")
        # self.out.branch("max_CSVV2","F")
        # self.out.branch("max_DeepB","F")
        self.out.branch("channel_mark","i")
        self.out.branch("nJets","i")

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
        loose_but_not_tight_muons = []
        loose_but_not_tight_electrons = []

        # selection on MET. Pass to next event directly if fail.
        if hasattr(event, "MET_T1Smear_pt"):
            self.out.fillBranch("MET",event.MET_T1Smear_pt)
        else:
            self.out.fillBranch("MET",event.MET_pt)


        #selection on muons
        for i in range(0,len(muons)):
            if muons[i].pt < 10:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].pfRelIso04_all < 0.4:
                loose_but_not_tight_muons.append(i)


        # selection on electrons
        for i in range(0,len(electrons)):
            if electrons[i].pt < 10:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) >  2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        if len(loose_but_not_tight_muons) + len(loose_but_not_tight_electrons) != 0:
            self.out.fillBranch("have_loose_lep", 1)
        else:
            self.out.fillBranch("have_loose_lep", 0)

        if len(tight_electrons)+len(tight_muons) < 3:
            return False
        elif len(tight_electrons)+len(tight_muons) > 3:
            self.out.fillBranch("More_than_three_tight_lep", 1)
            return True 
        elif len(tight_electrons)+len(tight_muons) == 3:
            self.out.fillBranch("More_than_three_tight_lep", 0)

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

            if photons[i].cutBased < 2:
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

            tight_photons.append(i)


        #dilepton mass selection and channel selection
        channel = 0 
        # emumu:     1
        # muee:      2
        # eee:       3 
        # mumumu:    4 

        # emumu
        dileptonmass = -1.0
        if len(tight_muons)==2 and len(tight_electrons)==1:  # emumu channel 
            if muons[tight_muons[0]].pdgId == -muons[tight_muons[1]].pdgId:

                if muons[tight_muons[0]].pt < 25:
                    return False
                if electrons[tight_electrons[0]].pt < 25:
                    return False

                dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                # if dileptonmass >= 60 and dileptonmass <= 120:
                # print "a=",tight_photons, "e=",tight_electrons, "mu=",tight_muons
            if dileptonmass < 4: 
                return False
            
            channel = 1


        # muee
        if len(tight_muons)==1 and len(tight_electrons)==2:
            if electrons[tight_electrons[0]].pdgId == -electrons[tight_electrons[1]].pdgId:

                if muons[tight_muons[0]].pt < 25:
                    return False
                if electrons[tight_electrons[0]].pt < 25:
                    return False

                dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
            if dileptonmass < 4: 
                return False
            
            channel = 2


        # eee 
        if len(tight_electrons)==3 and len(tight_muons)==0:
            # move the different charge lepton to the end for further analysis
            if electrons[tight_electrons[0]].charge == -electrons[tight_electrons[1]].charge:
                if electrons[tight_electrons[0]].charge == electrons[tight_electrons[2]].charge:
                    tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1] # e.g. +-+ -> ++-
                else:
                    tight_electrons[0],tight_electrons[2] = tight_electrons[2],tight_electrons[0] # e.g. -++ -> ++-
            else:
                if electrons[tight_electrons[0]].charge == electrons[tight_electrons[2]].charge:
                    return False                                                      # reject events for +++/---
            
            # compute mll and compare to mz, leptons with cloest mll to mz are considered to be z_leptons. Remaining lepton is w_lepton.
            mll13 = -1.0
            mll23 = -1.0
            mll13 = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[2]].p4()).M()
            mll23 = (electrons[tight_electrons[1]].p4() + electrons[tight_electrons[2]].p4()).M()
            if abs(mll13 - 91.188) > abs(mll23 - 91.188):
                dileptonmass = mll23
                if electrons[tight_electrons[1]].pt < electrons[tight_electrons[2]].pt:
                    tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1]
            else:
                tight_electrons[0],tight_electrons[1] = tight_electrons[1],tight_electrons[0] # move the w_lepton to the first one
                dileptonmass = mll13
                if electrons[tight_electrons[1]].pt < electrons[tight_electrons[2]].pt:
                    tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1]
            
            if electrons[tight_electrons[0]].pt < 25:
                return False
            if (electrons[tight_electrons[1]].pt < 25) and (electrons[tight_electrons[2]].pt < 25):
                return False

            if dileptonmass < 4: 
                return False

            channel = 3


        # mumumu
        if len(tight_muons)==3 and len(tight_electrons)==0:
            # move the different charge lepton to the end for further analysis
            if muons[tight_muons[0]].charge == -muons[tight_muons[1]].charge:
                if muons[tight_muons[0]].charge == muons[tight_muons[2]].charge:
                    tight_muons[1],tight_muons[2] = tight_muons[2],tight_muons[1] # e.g. +-+ -> ++-
                else:
                    tight_muons[0],tight_muons[2] = tight_muons[2],tight_muons[0] # e.g. -++ -> ++-
            else:
                if muons[tight_muons[0]].charge == muons[tight_muons[2]].charge:
                    return False                                                      # reject events for +++/---
            
            # compute mll and compare to mz, leptons with cloest mll to mz are considered to be z_leptons. Remaining lepton is w_lepton.
            mll13 = -1.0
            mll23 = -1.0
            mll13 = (muons[tight_muons[0]].p4() + muons[tight_muons[2]].p4()).M()
            mll23 = (muons[tight_muons[1]].p4() + muons[tight_muons[2]].p4()).M()
            if abs(mll13 - 91.188) > abs(mll23 - 91.188):
                dileptonmass = mll23
                if muons[tight_muons[1]].pt < muons[tight_muons[2]].pt:
                    tight_muons[1],tight_muons[2] = tight_muons[2], tight_muons[1]
            else:
                tight_muons[0],tight_muons[1] = tight_muons[1],tight_muons[0] # move the w_lepton to the first one
                dileptonmass = mll13
                if muons[tight_muons[1]].pt < muons[tight_muons[2]].pt:
                    tight_muons[1],tight_muons[2] = tight_muons[2], tight_muons[1]
            
            if muons[tight_muons[0]].pt < 25:
                return False
            if (muons[tight_muons[1]].pt < 25) and (muons[tight_muons[1]].pt < 25):
                return False

            if dileptonmass < 4: 
                return False

            channel = 4
#    test 
        if channel == 0:
            return False

        nJets = 0
        for i in range(0,len(jets)): 

            if jets[i].pt < 10:
                continue

            if abs(jets[i].eta) > 2.4:
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

            if jets[i].btagDeepB > 0.7665:
                nJets += 1


        if len(tight_photons) == 0:
            self.out.fillBranch("photon_mark", 0)
            self.out.fillBranch("photon_pt", 0)
            self.out.fillBranch("photon_eta", 0)
            self.out.fillBranch("photon_phi", 0)
            self.out.fillBranch("photon_mass", 0)
            self.out.fillBranch("photon_genPartFlav",-1)
        else:
            self.out.fillBranch("photon_mark", 1)
            self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
            self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
            self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
            self.out.fillBranch("photon_mass",photons[tight_photons[0]].mass)
            if hasattr(photons[tight_photons[0]], "genPartFlav"):
                self.out.fillBranch("photon_genPartFlav",photons[tight_photons[0]].genPartFlav)
            else:
                self.out.fillBranch("photon_genPartFlav",-1)
            if channel == 1:
                self.out.fillBranch("w_lepton_pt",  electrons[tight_electrons[0]].pt)
                self.out.fillBranch("w_lepton_eta", electrons[tight_electrons[0]].eta)
                self.out.fillBranch("w_lepton_phi", electrons[tight_electrons[0]].phi)
                self.out.fillBranch("w_lepton_mass", electrons[tight_electrons[0]].mass)
                self.out.fillBranch("z_lepton1_pt", muons[tight_muons[0]].pt)
                self.out.fillBranch("z_lepton1_eta",muons[tight_muons[0]].eta)
                self.out.fillBranch("z_lepton1_phi",muons[tight_muons[0]].phi)
                self.out.fillBranch("z_lepton1_mass",muons[tight_muons[0]].mass)
                self.out.fillBranch("z_lepton2_pt", muons[tight_muons[1]].pt)
                self.out.fillBranch("z_lepton2_eta",muons[tight_muons[1]].eta)
                self.out.fillBranch("z_lepton2_phi",muons[tight_muons[1]].phi)
                self.out.fillBranch("z_lepton2_mass",muons[tight_muons[1]].mass)
                if hasattr(muons[tight_muons[0]], "genPartFlav"):
                    self.out.fillBranch("w_lepton_genPartFlav",electrons[tight_electrons[0]].genPartFlav)
                    self.out.fillBranch("z_lepton1_genPartFlav",muons[tight_muons[0]].genPartFlav)
                    self.out.fillBranch("z_lepton2_genPartFlav",muons[tight_muons[1]].genPartFlav)
            elif channel == 2:
                self.out.fillBranch("w_lepton_pt",  muons[tight_muons[0]].pt)
                self.out.fillBranch("w_lepton_eta", muons[tight_muons[0]].eta)
                self.out.fillBranch("w_lepton_phi", muons[tight_muons[0]].phi)
                self.out.fillBranch("w_lepton_mass", muons[tight_muons[0]].mass)
                self.out.fillBranch("z_lepton1_pt", electrons[tight_electrons[0]].pt)
                self.out.fillBranch("z_lepton1_eta",electrons[tight_electrons[0]].eta)
                self.out.fillBranch("z_lepton1_phi",electrons[tight_electrons[0]].phi)
                self.out.fillBranch("z_lepton1_mass",electrons[tight_electrons[0]].mass)
                self.out.fillBranch("z_lepton2_pt", electrons[tight_electrons[1]].pt)
                self.out.fillBranch("z_lepton2_eta",electrons[tight_electrons[1]].eta)
                self.out.fillBranch("z_lepton2_phi",electrons[tight_electrons[1]].phi)
                self.out.fillBranch("z_lepton2_mass",electrons[tight_electrons[1]].mass)
                if hasattr(muons[tight_muons[0]], "genPartFlav"):
                    self.out.fillBranch("w_lepton_genPartFlav",muons[tight_muons[0]].genPartFlav)
                    self.out.fillBranch("z_lepton1_genPartFlav",electrons[tight_electrons[0]].genPartFlav)
                    self.out.fillBranch("z_lepton2_genPartFlav",electrons[tight_electrons[1]].genPartFlav)
            elif channel == 3:
                self.out.fillBranch("w_lepton_pt",  electrons[tight_electrons[0]].pt)
                self.out.fillBranch("w_lepton_eta", electrons[tight_electrons[0]].eta)
                self.out.fillBranch("w_lepton_phi", electrons[tight_electrons[0]].phi)
                self.out.fillBranch("w_lepton_mass", electrons[tight_electrons[0]].mass)
                self.out.fillBranch("z_lepton1_pt", electrons[tight_electrons[1]].pt)
                self.out.fillBranch("z_lepton1_eta",electrons[tight_electrons[1]].eta)
                self.out.fillBranch("z_lepton1_phi",electrons[tight_electrons[1]].phi)
                self.out.fillBranch("z_lepton1_mass",electrons[tight_electrons[1]].mass)
                self.out.fillBranch("z_lepton2_pt", electrons[tight_electrons[2]].pt)
                self.out.fillBranch("z_lepton2_eta",electrons[tight_electrons[2]].eta)
                self.out.fillBranch("z_lepton2_phi",electrons[tight_electrons[2]].phi)
                self.out.fillBranch("z_lepton2_mass",electrons[tight_electrons[2]].mass)
                if hasattr(electrons[tight_electrons[0]], "genPartFlav"):
                    self.out.fillBranch("w_lepton_genPartFlav",electrons[tight_electrons[0]].genPartFlav)
                    self.out.fillBranch("z_lepton1_genPartFlav",electrons[tight_electrons[1]].genPartFlav)
                    self.out.fillBranch("z_lepton2_genPartFlav",electrons[tight_electrons[2]].genPartFlav)
            elif channel == 4:
                self.out.fillBranch("w_lepton_pt",  muons[tight_muons[0]].pt)
                self.out.fillBranch("w_lepton_eta", muons[tight_muons[0]].eta)
                self.out.fillBranch("w_lepton_phi", muons[tight_muons[0]].phi)
                self.out.fillBranch("w_lepton_mass", muons[tight_muons[0]].mass)
                self.out.fillBranch("z_lepton1_pt", muons[tight_muons[1]].pt)
                self.out.fillBranch("z_lepton1_eta",muons[tight_muons[1]].eta)
                self.out.fillBranch("z_lepton1_phi",muons[tight_muons[1]].phi)
                self.out.fillBranch("z_lepton1_mass",muons[tight_muons[1]].mass)
                self.out.fillBranch("z_lepton2_pt", muons[tight_muons[2]].pt)
                self.out.fillBranch("z_lepton2_eta",muons[tight_muons[2]].eta)
                self.out.fillBranch("z_lepton2_phi",muons[tight_muons[2]].phi)
                self.out.fillBranch("z_lepton2_mass",muons[tight_muons[2]].mass)
                if hasattr(muons[tight_muons[0]], "genPartFlav"):
                    self.out.fillBranch("w_lepton_genPartFlav",muons[tight_muons[0]].genPartFlav)
                    self.out.fillBranch("z_lepton1_genPartFlav",muons[tight_muons[1]].genPartFlav)
                    self.out.fillBranch("z_lepton2_genPartFlav",muons[tight_muons[2]].genPartFlav)

        self.out.fillBranch("dilepton_mass",dileptonmass)
        if hasattr(event, "Generator_weight"):
            self.out.fillBranch("Generator_weight",event.Generator_weight)
        else:
            self.out.fillBranch("Generator_weight",0)
        self.out.fillBranch("channel_mark",channel)
        self.out.fillBranch("nJets",nJets)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

WZG_select_Module = lambda : WZG_Producer()