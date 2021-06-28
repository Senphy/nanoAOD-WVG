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


test=0
MET_pass = 0
photon_pass = 0
electron_pass = 0
muon_pass = 0
none_lepton_reject = 0
none_3lepton_reject = 0
dilepton_pass = 0
emumu_pass = 0
eee_pass = 0
muee_pass = 0
mumumu_pass = 0
btagjet_reject = 0
none_photon_reject = 0
same_charge_reject_eee = 0
same_charge_reject_mumumu = 0

class HLT_template_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("event",  "l")
        self.out.branch("MET",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("photon_genPartFlav",  "I")
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
        # Record the pass numbers for each cut. Noticed that for efficiency, those who can't pass the MET cut may not be counted because it will pass to next event directly.

        global MET_pass
        global photon_pass
        global electron_pass
        global muon_pass
        global none_lepton_reject
        global none_3lepton_reject
        global dilepton_pass
        global emumu_pass 
        global eee_pass 
        global muee_pass 
        global mumumu_pass 
        global btagjet_reject
        global test
        global none_photon_reject
        global same_charge_reject_eee
        global same_charge_reject_mumumu
        test += 1


        # selection on MET. Pass to next event directly if fail.
        # if  event.MET_pt > 20:
        #     MET_pass += 1
        # else:
        #     return False  


        #selection on muons
        for i in range(0,len(muons)):
            if muons[i].pt < 10:
                continue
            if abs(muons[i].eta) > 2.5:
                continue
            if abs(muons[i].dz) > 0.1 or abs(muons[i].dxy) > 0.05:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
                muon_pass += 1
            elif muons[i].tightId and muons[i].pfRelIso04_all < 0.4:
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
                    electron_pass += 1
                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)


        if len(tight_electrons)==0 and len(tight_muons)==0:      #reject event if there is no lepton selected in the event
            none_lepton_reject += 1
            return False
        
        if len(tight_electrons)+len(tight_muons) != 3:      #reject event if there are not exactly three leptons
            none_3lepton_reject += 1
            return False

        if len(loose_but_not_tight_electrons)+len(loose_but_not_tight_muons) !=0: # 4th lep veto
            return False

        # selection on photons
        # for i in range(0,len(photons)):

            # This condition should be changed for different process
            #  photons[i].genPartFlav == 1:
                # continue

        #     if photons[i].pt < 20:
        #         continue

        #     if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
        #         continue

        #     if not ((abs(photons[i].eta) < 1.4442) or (1.566 < abs(photons[i].eta) and abs(photons[i].eta) < 2.5) ):
        #         continue

        #     if photons[i].pixelSeed:
        #         continue

        #     if photons[i].cutBased < 2:
        #         continue

        #     pass_lepton_dr_cut = True

        #     for j in range(0,len(tight_muons)):
        #         if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
        #             pass_lepton_dr_cut = False

        #     for j in range(0,len(tight_electrons)):
        #         if deltaR(electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
        #             pass_lepton_dr_cut = False

        #     if not pass_lepton_dr_cut:
        #         continue

        #     tight_photons.append(i)
        #     photon_pass += 1

        # if len(tight_photons)==0:
        #    none_photon_reject +=1 
        #    return False                        #reject event if there is not exact one photon in the event 


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

                # if muons[tight_muons[0]].pt < 25:
                #     return False
                # if electrons[tight_electrons[0]].pt < 25:
                #     return False

                dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                # if dileptonmass >= 60 and dileptonmass <= 120:
                # print "a=",tight_photons, "e=",tight_electrons, "mu=",tight_muons
            if dileptonmass < 4: 
                return False
            
            channel = 1
            emumu_pass += 1


        # muee
        if len(tight_muons)==1 and len(tight_electrons)==2:
            if electrons[tight_electrons[0]].pdgId == -electrons[tight_electrons[1]].pdgId:

                # if muons[tight_muons[0]].pt < 25:
                #     return False
                # if electrons[tight_electrons[0]].pt < 25:
                #     return False

                dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
            if dileptonmass < 4: 
                return False
            
            channel = 2
            muee_pass += 1


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
                    same_charge_reject_eee +=1
                    return False                                                      # reject events for +++/---
            
            # compute mll and compare to mz, leptons with cloest mll to mz are considered to be z_leptons. Remaining lepton is w_lepton.
            mll13 = -1.0
            mll23 = -1.0
            mll13 = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[2]].p4()).M()
            mll23 = (electrons[tight_electrons[1]].p4() + electrons[tight_electrons[2]].p4()).M()
            if abs(mll13 - 91.188) > abs(mll23 - 91.188):
                dileptonmass = mll23
                if electrons[tight_electrons[1]].pt < electrons[tight_electrons[2]].pt:
                    tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1] # let z1_pt > z2_pt
            else:
                tight_electrons[0],tight_electrons[1] = tight_electrons[1],tight_electrons[0] # move the w_lepton to the first one
                dileptonmass = mll13
                if electrons[tight_electrons[1]].pt < electrons[tight_electrons[2]].pt:
                    tight_electrons[1],tight_electrons[2] = tight_electrons[2],tight_electrons[1]
            
            # if electrons[tight_electrons[0]].pt < 25:
            #     return False
            # if (electrons[tight_electrons[1]].pt < 25) and (electrons[tight_electrons[2]].pt < 25):
            #     return False

            if dileptonmass < 4: 
                return False

            channel = 3
            eee_pass += 1


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
                    same_charge_reject_mumumu += 1
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
            
            # if muons[tight_muons[0]].pt < 25:
            #     return False
            # if (muons[tight_muons[1]].pt < 25) and (muons[tight_muons[1]].pt < 25):
            #     return False

            if dileptonmass < 4: 
                return False

            channel = 4
            mumumu_pass += 1
#    test 
        if channel == 0:
            return False

        # nJets = 0
        # for i in range(0,len(jets)): 

        #     if jets[i].pt < 10:
        #         continue

        #     if abs(jets[i].eta) > 4.7:
        #         continue

        #     pass_lepton_dr_cut = True

        #     for j in range(0,len(tight_photons)):
        #         if deltaR(jets[i].eta,jets[i].phi,photons[tight_photons[j]].eta,photons[tight_photons[j]].phi) < 0.5:
        #             pass_lepton_dr_cut = False

        #     for j in range(0,len(tight_electrons)):
        #         if deltaR(jets[i].eta,jets[i].phi,electrons[tight_electrons[j]].eta,electrons[tight_electrons[j]].phi) < 0.5:
        #             pass_lepton_dr_cut = False

        #     for j in range(0,len(tight_muons)):
        #         if deltaR(jets[i].eta,jets[i].phi,muons[tight_muons[j]].eta,muons[tight_muons[j]].phi) < 0.5:
        #             pass_lepton_dr_cut = False

        #     if not pass_lepton_dr_cut: 
        #         continue

        #     if jets[i].btagDeepB > 0.7665:
        #         nJets += 1


        # self.out.fillBranch("photon_pt",photons[tight_photons[0]].pt)
        # self.out.fillBranch("photon_eta",photons[tight_photons[0]].eta)
        # self.out.fillBranch("photon_phi",photons[tight_photons[0]].phi)
        # if hasattr(photons[tight_photons[0]], "genPartFlav"):
        #     self.out.fillBranch("photon_genPartFlav",photons[tight_photons[0]].genPartFlav)
        # else:
        #     self.out.fillBranch("photon_genPartFlav",-1)
        if channel == 1:
            self.out.fillBranch("w_lepton_pt",  electrons[tight_electrons[0]].pt)
            self.out.fillBranch("w_lepton_eta", electrons[tight_electrons[0]].eta)
            self.out.fillBranch("w_lepton_phi", electrons[tight_electrons[0]].phi)
            self.out.fillBranch("z_lepton1_pt", muons[tight_muons[0]].pt)
            self.out.fillBranch("z_lepton1_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("z_lepton1_phi",muons[tight_muons[0]].phi)
            self.out.fillBranch("z_lepton2_pt", muons[tight_muons[1]].pt)
            self.out.fillBranch("z_lepton2_eta",muons[tight_muons[1]].eta)
            self.out.fillBranch("z_lepton2_phi",muons[tight_muons[1]].phi)
        elif channel == 2:
            self.out.fillBranch("w_lepton_pt",  muons[tight_muons[0]].pt)
            self.out.fillBranch("w_lepton_eta", muons[tight_muons[0]].eta)
            self.out.fillBranch("w_lepton_phi", muons[tight_muons[0]].phi)
            self.out.fillBranch("z_lepton1_pt", electrons[tight_electrons[0]].pt)
            self.out.fillBranch("z_lepton1_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("z_lepton1_phi",electrons[tight_electrons[0]].phi)
            self.out.fillBranch("z_lepton2_pt", electrons[tight_electrons[1]].pt)
            self.out.fillBranch("z_lepton2_eta",electrons[tight_electrons[1]].eta)
            self.out.fillBranch("z_lepton2_phi",electrons[tight_electrons[1]].phi)
        elif channel == 3:
            self.out.fillBranch("w_lepton_pt",  electrons[tight_electrons[0]].pt)
            self.out.fillBranch("w_lepton_eta", electrons[tight_electrons[0]].eta)
            self.out.fillBranch("w_lepton_phi", electrons[tight_electrons[0]].phi)
            self.out.fillBranch("z_lepton1_pt", electrons[tight_electrons[1]].pt)
            self.out.fillBranch("z_lepton1_eta",electrons[tight_electrons[1]].eta)
            self.out.fillBranch("z_lepton1_phi",electrons[tight_electrons[1]].phi)
            self.out.fillBranch("z_lepton2_pt", electrons[tight_electrons[2]].pt)
            self.out.fillBranch("z_lepton2_eta",electrons[tight_electrons[2]].eta)
            self.out.fillBranch("z_lepton2_phi",electrons[tight_electrons[2]].phi)
        elif channel == 4:
            self.out.fillBranch("w_lepton_pt",  muons[tight_muons[0]].pt)
            self.out.fillBranch("w_lepton_eta", muons[tight_muons[0]].eta)
            self.out.fillBranch("w_lepton_phi", muons[tight_muons[0]].phi)
            self.out.fillBranch("z_lepton1_pt", muons[tight_muons[1]].pt)
            self.out.fillBranch("z_lepton1_eta",muons[tight_muons[1]].eta)
            self.out.fillBranch("z_lepton1_phi",muons[tight_muons[1]].phi)
            self.out.fillBranch("z_lepton2_pt", muons[tight_muons[2]].pt)
            self.out.fillBranch("z_lepton2_eta",muons[tight_muons[2]].eta)
            self.out.fillBranch("z_lepton2_phi",muons[tight_muons[2]].phi)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("dilepton_mass",dileptonmass)
        if hasattr(event, "Generator_weight"):
            self.out.fillBranch("Generator_weight",event.Generator_weight)
        else:
            self.out.fillBranch("Generator_weight",0)
        self.out.fillBranch("channel_mark",channel)
        self.out.fillBranch("MET",event.MET_pt)
        # self.out.fillBranch("nJets",nJets)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

# WZG_Module = lambda : WZG_Producer()