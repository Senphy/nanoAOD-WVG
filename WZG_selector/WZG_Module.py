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

class WZG_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("event",  "i")
        self.out.branch("MET",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_phi",  "F")
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
        photons_select = []
        electrons_select = []
        tight_muons = [] 
        loose_but_not_tight_muons = []
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
        if  event.MET_pt>20:
            self.out.fillBranch("MET",event.MET_pt)
            MET_pass += 1
        else:
            return False  


        #selection on muons
        for i in range(0,len(muons)):
            if muons[i].pt < 20:
                continue
            if abs(muons[i].eta) > 2.5:
                continue
            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
                muon_pass += 1
            elif muons[i].pfRelIso04_all < 0.4
                loose_but_not_tight_muons.append(i)


        # selection on electrons
        for i in range(0,len(electrons)):
            if electrons[i].pt < 20:
                continue
            if abs(electrons[i].eta) >  2.5:
                continue
            if electrons[i].cutBased >= 3:
                electrons_select.append(i)
                electron_pass += 1


        # selection on photons
        for i in range(0,len(photons)):
            if not photons[i].electronVeto:
                continue
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue

            pass_lepton_dr_cut = True
            for j in range(0,len(tight_muons)):
                if deltaR(muons[tight_muons[j]].eta,muons[tight_muons[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            if not pass_lepton_dr_cut:
                continue

            photons_select.append(i)
            photon_pass += 1

        if not len(photons_select)==1:
           none_photon_reject +=1 
           return False                        #reject event if there is not exact one photon in the event 


        if len(electrons_select)==0 and len(tight_muons)==0:      #reject event if there is no lepton selected in the event
            none_lepton_reject += 1
            return False
        
        if len(electrons_select)+len(tight_muons) != 3:      #reject event if there are not exactly three leptons
            none_3lepton_reject += 1
            return False

        #dilepton mass selection and channel selection
        channel = 0 
        # emumu:     1
        # muee:      2
        # eee:       3 
        # mumumu:    4 

        # emumu
        dileptonmass = -1.0
        if len(tight_muons)==2 and len(electrons_select)==1:  # emumu channel 
            if muons[tight_muons[0]].pdgId == -muons[tight_muons[1]].pdgId:
                dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                # if dileptonmass >= 60 and dileptonmass <= 120:
                # print "a=",photons_select, "e=",electrons_select, "mu=",tight_muons
            if dileptonmass >= 0: 
                channel = 1
                emumu_pass += 1

        # muee
        if len(tight_muons)==1 and len(electrons_select)==2:
            if electrons[electrons_select[0]].pdgId == -electrons[electrons_select[1]].pdgId:
                dileptonmass = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).M()
            if dileptonmass >= 0:
                channel = 2
                muee_pass += 1

        # eee 
        if len(electrons_select)==3 and len(tight_muons)==0:
            # move the different charge lepton to the end for further analysis
            if electrons[electrons_select[0]].charge == -electrons[electrons_select[1]].charge:
                if electrons[electrons_select[0]].charge == electrons[electrons_select[2]].charge:
                    electrons_select[1],electrons_select[2] = electrons_select[2],electrons_select[1] # e.g. +-+ -> ++-
                else:
                    electrons_select[0],electrons_select[2] = electrons_select[2],electrons_select[0] # e.g. -++ -> ++-
            else:
                if electrons[electrons_select[0]].charge == electrons[electrons_select[2]].charge:
                    same_charge_reject_eee +=1
                    return False                                                      # reject events for +++/---
            
            # compute mll and compare to mz, leptons with cloest mll to mz are considered to be z_leptons. Remaining lepton is w_lepton.
            mll13 = -1.0
            mll23 = -1.0
            mll13 = (electrons[electrons_select[0]].p4() + electrons[electrons_select[2]].p4()).M()
            mll23 = (electrons[electrons_select[1]].p4() + electrons[electrons_select[2]].p4()).M()
            if abs(mll13 - 91.188) > abs(mll23 - 91.188):
                dileptonmass = mll23
            else:
                electrons_select[0],electrons_select[1] = electrons_select[1],electrons_select[0] # move the w_lepton to the first one
                dileptonmass = mll13
            
            if dileptonmass >= 0:
                channel = 3
                eee_pass += 1

        # mumumu
        if len(tight_muons)==3 and len(electrons_select)==0:
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
            else:
                tight_muons[0],tight_muons[1] = tight_muons[1],tight_muons[0] # move the w_lepton to the first one
                dileptonmass = mll13
            
            if dileptonmass >= 0:
                channel = 4
                mumumu_pass += 1
#    test 
        if channel == 0:
            return False

        # selection on b-tag jet
        for i in range(0,len(jets)): 
            btag_cut = False
            if jets[i].btagCMVA > -0.5884:  # cMVAv2L
            # if jets[i].btagCMVA > 0.4432:  # cMVAv2M
            # if jets[i].btagCSVV2 > 0.5426:  # CSVv2L
            # if jets[i].btagCSVV2 > 0.8484:  # CSVv2M
            # if jets[i].btagDeepB > 0.2219:  # DeepCSVL
            # if jets[i].btagDeepB > 0.6324:  # DeepCSVM
                btag_cut = True      #initialize
                if jets[i].pt<30:
                    continue
                for j in range(0,len(photons_select)):          # delta R cut, if all deltaR(lep,jet) and deltaR(gamma,jet)>0.3, consider jet as a b jet
                    if deltaR(jets[i].eta,jets[i].phi,photons[photons_select[j]].eta,photons[photons_select[j]].phi) < 0.3:
                        btag_cut = False
                for j in range(0,len(electrons_select)):
                    if deltaR(jets[i].eta,jets[i].phi,electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi) < 0.3:
                        btag_cut = False
                for j in range(0,len(tight_muons)):
                    if deltaR(jets[i].eta,jets[i].phi,muons[tight_muons[j]].eta,muons[tight_muons[j]].phi) < 0.3:
                        btag_cut = False
            if btag_cut == True:
                btagjet_reject += 1
                return False

        # max_CMVA=-999
        # max_CSVV2=-999
        # max_DeepB=-999
        # for i in range(0,len(jets)): 
        #     if jets[i].btagCMVA > max_CMVA: max_CMVA = jets[i].btagCMVA
        #     if jets[i].btagCSVV2 > max_CSVV2: max_CSVV2 = jets[i].btagCSVV2
        #     if jets[i].btagDeepB > max_DeepB: max_DeepB = jets[i].btagDeepB
        # self.out.fillBranch("max_CMVA",max_CMVA)
        # self.out.fillBranch("max_CSVV2",max_CSVV2)
        # self.out.fillBranch("max_DeepB",max_DeepB)



        self.out.fillBranch("photon_pt",photons[photons_select[0]].pt)
        self.out.fillBranch("photon_eta",photons[photons_select[0]].eta)
        self.out.fillBranch("photon_phi",photons[photons_select[0]].phi)
        if channel == 1:
            self.out.fillBranch("w_lepton_pt",  electrons[electrons_select[0]].pt)
            self.out.fillBranch("w_lepton_eta", electrons[electrons_select[0]].eta)
            self.out.fillBranch("w_lepton_phi", electrons[electrons_select[0]].phi)
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
            self.out.fillBranch("z_lepton1_pt", electrons[electrons_select[0]].pt)
            self.out.fillBranch("z_lepton1_eta",electrons[electrons_select[0]].eta)
            self.out.fillBranch("z_lepton1_phi",electrons[electrons_select[0]].phi)
            self.out.fillBranch("z_lepton2_pt", electrons[electrons_select[1]].pt)
            self.out.fillBranch("z_lepton2_eta",electrons[electrons_select[1]].eta)
            self.out.fillBranch("z_lepton2_phi",electrons[electrons_select[1]].phi)
        elif channel == 3:
            self.out.fillBranch("w_lepton_pt",  electrons[electrons_select[0]].pt)
            self.out.fillBranch("w_lepton_eta", electrons[electrons_select[0]].eta)
            self.out.fillBranch("w_lepton_phi", electrons[electrons_select[0]].phi)
            self.out.fillBranch("z_lepton1_pt", electrons[electrons_select[1]].pt)
            self.out.fillBranch("z_lepton1_eta",electrons[electrons_select[1]].eta)
            self.out.fillBranch("z_lepton1_phi",electrons[electrons_select[1]].phi)
            self.out.fillBranch("z_lepton2_pt", electrons[electrons_select[2]].pt)
            self.out.fillBranch("z_lepton2_eta",electrons[electrons_select[2]].eta)
            self.out.fillBranch("z_lepton2_phi",electrons[electrons_select[2]].phi)
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
        self.out.fillBranch("Generator_weight",event.Generator_weight)
        self.out.fillBranch("channel_mark",channel)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

# WZG_Module = lambda : WZG_Producer()