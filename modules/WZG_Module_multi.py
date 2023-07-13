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


class WZG_multi_Producer(Module):
    def __init__(self):
        pass
    def ZZ_GetLepIndex(self, abs_mll_mz):
        lepton_index_mark = abs_mll_mz.index(min(abs_mll_mz))
        lepton_map = {0:[0,1], 1:[0,2], 2:[0,3], 3:[1,2], 4:[1,3], 5:[2,3]}
        l1_index = lepton_map[lepton_index_mark][0]
        l2_index = lepton_map[lepton_index_mark][1]
        l3_index = [x for x in range(0,4) if x not in lepton_map[lepton_index_mark]][0]
        l4_index = [x for x in range(0,4) if x not in lepton_map[lepton_index_mark]][1]
        return (l1_index, l2_index, l3_index, l4_index)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MET",  "F")
        self.out.branch("channel_mark","i")
        self.out.branch("region_mark","i")
        self.out.branch("dr_wla", "F")
        self.out.branch("dr_zl1a", "F")
        self.out.branch("dr_zl2a", "F")
        self.out.branch("mwa", "F")

        self.out.branch("ZGJ_lepton1_pt",  "F")
        self.out.branch("ZGJ_lepton1_eta",  "F")
        self.out.branch("ZGJ_lepton1_phi",  "F")
        self.out.branch("ZGJ_lepton1_mass",  "F")
        self.out.branch("ZGJ_lepton1_genPartFlav",  "i")
        self.out.branch("ZGJ_lepton1_index",  "i")
        self.out.branch("ZGJ_lepton2_pt",  "F")
        self.out.branch("ZGJ_lepton2_eta",  "F")
        self.out.branch("ZGJ_lepton2_phi",  "F")
        self.out.branch("ZGJ_lepton2_mass",  "F")
        self.out.branch("ZGJ_lepton2_genPartFlav",  "i")
        self.out.branch("ZGJ_lepton2_index",  "i")
        self.out.branch("ZGJ_photon_pt",  "F")
        self.out.branch("ZGJ_photon_eta",  "F")
        self.out.branch("ZGJ_photon_phi",  "F")
        self.out.branch("ZGJ_photon_mass",  "F")
        self.out.branch("ZGJ_photon_genPartFlav",  "i")
        self.out.branch("ZGJ_photon_index",  "i")
        self.out.branch("ZGJ_photon_vidNestedWPBitmap",  "L")
        self.out.branch("ZGJ_photon_pfRelIso03_chg", "F")
        self.out.branch("ZGJ_photon_sieie", "F")
        self.out.branch("ZGJ_dileptonmass",  "F")
        self.out.branch("ZGJ_mlla",  "F")

        self.out.branch("ZZ_lepton1_pt",  "F")
        self.out.branch("ZZ_lepton1_eta",  "F")
        self.out.branch("ZZ_lepton1_phi",  "F")
        self.out.branch("ZZ_lepton1_mass",  "F")
        self.out.branch("ZZ_lepton1_genPartFlav",  "i")
        self.out.branch("ZZ_lepton1_index",  "i")
        self.out.branch("ZZ_lepton2_pt",  "F")
        self.out.branch("ZZ_lepton2_eta",  "F")
        self.out.branch("ZZ_lepton2_phi",  "F")
        self.out.branch("ZZ_lepton2_mass",  "F")
        self.out.branch("ZZ_lepton2_genPartFlav",  "i")
        self.out.branch("ZZ_lepton2_index",  "i")
        self.out.branch("ZZ_lepton3_pt",  "F")
        self.out.branch("ZZ_lepton3_eta",  "F")
        self.out.branch("ZZ_lepton3_phi",  "F")
        self.out.branch("ZZ_lepton3_mass",  "F")
        self.out.branch("ZZ_lepton3_genPartFlav",  "i")
        self.out.branch("ZZ_lepton3_index",  "i")
        self.out.branch("ZZ_lepton4_pt",  "F")
        self.out.branch("ZZ_lepton4_eta",  "F")
        self.out.branch("ZZ_lepton4_phi",  "F")
        self.out.branch("ZZ_lepton4_mass",  "F")
        self.out.branch("ZZ_lepton4_genPartFlav",  "i")
        self.out.branch("ZZ_lepton4_index",  "i")
        self.out.branch("ZZ_mllz1",  "F")
        self.out.branch("ZZ_mllz2",  "F")
        self.out.branch("ZZ_trileptonmass",  "F")
        self.out.branch("ZZ_MET",  "F")

        self.out.branch("WZG_lepton1_pt",  "F")
        self.out.branch("WZG_lepton1_eta",  "F")
        self.out.branch("WZG_lepton1_phi",  "F")
        self.out.branch("WZG_lepton1_mass",  "F")
        self.out.branch("WZG_lepton1_genPartFlav",  "i")
        self.out.branch("WZG_lepton1_index",  "i")
        self.out.branch("WZG_lepton2_pt",  "F")
        self.out.branch("WZG_lepton2_eta",  "F")
        self.out.branch("WZG_lepton2_phi",  "F")
        self.out.branch("WZG_lepton2_mass",  "F")
        self.out.branch("WZG_lepton2_genPartFlav",  "i")
        self.out.branch("WZG_lepton2_index",  "i")
        self.out.branch("WZG_lepton3_pt",  "F")
        self.out.branch("WZG_lepton3_eta",  "F")
        self.out.branch("WZG_lepton3_phi",  "F")
        self.out.branch("WZG_lepton3_mass",  "F")
        self.out.branch("WZG_lepton3_genPartFlav",  "i")
        self.out.branch("WZG_lepton3_index",  "i")
        self.out.branch("WZG_photon_pt",  "F")
        self.out.branch("WZG_photon_eta",  "F")
        self.out.branch("WZG_photon_phi",  "F")
        self.out.branch("WZG_photon_mass",  "F")
        self.out.branch("WZG_photon_genPartFlav",  "i")
        self.out.branch("WZG_photon_vidNestedWPBitmap",  "L")
        self.out.branch("WZG_photon_pfRelIso03_chg", "F")
        self.out.branch("WZG_photon_sieie", "F")
        self.out.branch("WZG_photon_index",  "i")
        self.out.branch("WZG_dileptonmass",  "F")
        self.out.branch("WZG_trileptonmass",  "F")
        self.out.branch("WZG_mlla",  "F")
        self.out.branch("WZG_MET",  "F")

        self.out.branch("ttG_lepton1_pt",  "F")
        self.out.branch("ttG_lepton1_eta",  "F")
        self.out.branch("ttG_lepton1_phi",  "F")
        self.out.branch("ttG_lepton1_mass",  "F")
        self.out.branch("ttG_lepton1_genPartFlav",  "i")
        self.out.branch("ttG_lepton1_index",  "i")
        self.out.branch("ttG_lepton2_pt",  "F")
        self.out.branch("ttG_lepton2_eta",  "F")
        self.out.branch("ttG_lepton2_phi",  "F")
        self.out.branch("ttG_lepton2_mass",  "F")
        self.out.branch("ttG_lepton2_genPartFlav",  "i")
        self.out.branch("ttG_lepton2_index",  "i")
        self.out.branch("ttG_lepton3_pt",  "F")
        self.out.branch("ttG_lepton3_eta",  "F")
        self.out.branch("ttG_lepton3_phi",  "F")
        self.out.branch("ttG_lepton3_mass",  "F")
        self.out.branch("ttG_lepton3_genPartFlav",  "i")
        self.out.branch("ttG_lepton3_index",  "i")
        self.out.branch("ttG_photon_pt",  "F")
        self.out.branch("ttG_photon_eta",  "F")
        self.out.branch("ttG_photon_phi",  "F")
        self.out.branch("ttG_photon_mass",  "F")
        self.out.branch("ttG_photon_genPartFlav",  "i")
        self.out.branch("ttG_photon_vidNestedWPBitmap",  "L")
        self.out.branch("ttG_photon_pfRelIso03_chg", "F")
        self.out.branch("ttG_photon_sieie", "F")
        self.out.branch("ttG_photon_index",  "i")
        self.out.branch("ttG_dileptonmass",  "F")
        self.out.branch("ttG_trileptonmass",  "F")
        self.out.branch("ttG_mlla",  "F")
        self.out.branch("ttG_MET",  "F")

        self.out.branch("ttZ_lepton1_pt",  "F")
        self.out.branch("ttZ_lepton1_eta",  "F")
        self.out.branch("ttZ_lepton1_phi",  "F")
        self.out.branch("ttZ_lepton1_mass",  "F")
        self.out.branch("ttZ_lepton1_genPartFlav",  "i")
        self.out.branch("ttZ_lepton1_index",  "i")
        self.out.branch("ttZ_lepton2_pt",  "F")
        self.out.branch("ttZ_lepton2_eta",  "F")
        self.out.branch("ttZ_lepton2_phi",  "F")
        self.out.branch("ttZ_lepton2_mass",  "F")
        self.out.branch("ttZ_lepton2_genPartFlav",  "i")
        self.out.branch("ttZ_lepton2_index",  "i")
        self.out.branch("ttZ_lepton3_pt",  "F")
        self.out.branch("ttZ_lepton3_eta",  "F")
        self.out.branch("ttZ_lepton3_phi",  "F")
        self.out.branch("ttZ_lepton3_mass",  "F")
        self.out.branch("ttZ_lepton3_genPartFlav",  "i")
        self.out.branch("ttZ_lepton3_index",  "i")
        self.out.branch("ttZ_dileptonmass",  "F")
        self.out.branch("ttZ_trileptonmass",  "F")
        self.out.branch("ttZ_MET",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        dileptonp4 = ROOT.TLorentzVector()

        # selection on MET. Pass to next event directly if fail.
        if hasattr(event, "MET_T1Smear_pt"):
            MET = event.MET_T1Smear_pt
            self.out.fillBranch("MET",event.MET_T1Smear_pt)
        else:
            MET = event.MET_pt
            self.out.fillBranch("MET",event.MET_pt)
        
        # Load Objects
        # *FIXME* Potential bugs here for TTreeArray conversion.
        # Can't run seperately without define_object module
        tight_muons = event.TightMuons_index[:event.nTightMuons]
        for i in tight_muons:
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())
        tight_electrons = event.TightElectrons_index[:event.nTightElectrons]
        tight_photons = event.TightPhotons_index[:event.nTightPhotons]
        tight_bjets = event.TightbJets_index[:event.nbJets]

        fake_muons = event.FakeMuons_index[:event.nFakeMuons]
        for i in fake_muons:
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())
        fake_electrons = event.FakeElectrons_index[:event.nFakeElectrons]
        fake_photons = event.FakePhotons_index[:event.nFakePhotons]

        veto_muons = event.VetoMuons_index[:event.nVetoMuons]
        for i in veto_muons:
            muons[i].p4().SetPtEtaPhiM(event.Muon_corrected_pt[i], muons[i].p4().Eta(), muons[i].p4().Phi(), muons[i].p4().M())
        veto_electrons = event.VetoElectrons_index[:event.nVetoElectrons]

        ntightandfakeleptons = len(tight_electrons) + len(tight_muons) + len(fake_muons) + len(fake_electrons)
        ntightleptons = len(tight_electrons) + len(tight_muons)
        nfakeleptons = len(fake_electrons) + len(fake_muons)

        # region mark
        # 1: nominal
        # 2: Fake Lep AR
            # nonprompt lepton application region
            # others are same with Signal Region except:
            # At least one lepton fail tight selection but pass loose selection
        # 3: Fake Pho AR
            # nonprompt photon application region
            # others are same with Signal Region except:
            # At least one photon, with sieie cut removed
        region_mark = 1

        channel = -99 
        # 1: WZG_emm
        # 2: WZG_mee
        # 3: WZG_eee
        # 4: WZG_mmm
        # 11: ttZ_emm
        # 12: ttZ_mee
        # 13: ttZ_eee
        # 14: ttZ_mmm
        # 21: ttG_emm
        # 22: ttG_mee
        # 23: ttG_eee
        # 24: ttG_mmm
        # 5: ZZ_eemm
        # 6: ZZ_mmee
        # 7: ZZ_eeee
        # 8: ZZ_mmmm        
        # 31: ZGJets_ee
        # 32: ZGJets_mm


        # ZGJets Control Region
        # Zjets + photon region is designed to validate nonprompt photon.
        # |mll-mz| > 15
        # min mll > 4
        # >=0 tight photon
        # >0 b jets
        # MET < 40

        # two leptons situation, denote fake lepton as f, tight as t
        # (ff + tf + ft + tt)
        if (ntightandfakeleptons == 2):

            # OSSF selection has been added in pre-selection module
            if len(tight_photons) + len(fake_photons) == 0:
                return False

            # tt plus nf, if n=0 region 1 else veto
            if ntightleptons == 2:
                if len(fake_muons) + len(fake_electrons) + len(veto_muons) + len(veto_electrons) != 0:
                    return False

            # Check if it is ff/tf/ft set it as region 2
            if len(fake_muons) + len(fake_electrons) != 0:
                region_mark = 2
                # Merge tight and fake for convenience
                tight_muons = tight_muons + fake_muons
                tight_muons.sort(key=lambda x: muons[x].pt, reverse=True)
                tight_electrons = tight_electrons + fake_electrons
                tight_electrons.sort(key=lambda x: electrons[x].pt, reverse=True)
            
            # check if fake photons exist
            if len(fake_photons) != 0:
                if len(tight_photons) == 0:
                    # Remove events with no tight photons in ff/tf/ft
                    if region_mark == 2:
                        return False
                    # (tt) or (tt plus nf) with only fake photons = region 3
                    # Merge tight and fake for convenience
                    region_mark = 3
                    tight_photons = tight_photons + fake_photons
                    tight_photons.sort(key=lambda x: photons[x].pt, reverse=True)
                elif photons[tight_photons[0]].pt < photons[fake_photons[0]].pt:
                    # ff/tf/ft with tight photons included = region 2
                    if region_mark == 2:
                        pass
                    # *FIXME* tt with leading fake photon still = region 1
                    # TBD, a potential overlap problem here
                    else:
                        pass
                else:
                    pass

            if len(tight_electrons) == 2:
                dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
                m_lla = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4() + photons[tight_photons[0]].p4()).M()
                self.out.fillBranch("channel_mark", 31)
                self.out.fillBranch("region_mark", region_mark)
                self.out.fillBranch("ZGJ_lepton1_pt", electrons[tight_electrons[0]].pt)
                self.out.fillBranch("ZGJ_lepton1_eta", electrons[tight_electrons[0]].eta)
                self.out.fillBranch("ZGJ_lepton1_phi", electrons[tight_electrons[0]].phi)
                self.out.fillBranch("ZGJ_lepton1_mass", electrons[tight_electrons[0]].mass)
                self.out.fillBranch("ZGJ_lepton1_index", tight_electrons[0])
                self.out.fillBranch("ZGJ_lepton2_pt", electrons[tight_electrons[1]].pt)
                self.out.fillBranch("ZGJ_lepton2_eta", electrons[tight_electrons[1]].eta)
                self.out.fillBranch("ZGJ_lepton2_phi", electrons[tight_electrons[1]].phi)
                self.out.fillBranch("ZGJ_lepton2_mass", electrons[tight_electrons[1]].mass)
                self.out.fillBranch("ZGJ_lepton2_index", tight_electrons[1])
                self.out.fillBranch("ZGJ_dileptonmass", dileptonmass)
                self.out.fillBranch("ZGJ_mlla", m_lla)
                self.out.fillBranch("ZGJ_photon_pt", photons[tight_photons[0]].pt)
                self.out.fillBranch("ZGJ_photon_eta", photons[tight_photons[0]].eta)
                self.out.fillBranch("ZGJ_photon_phi", photons[tight_photons[0]].phi)
                self.out.fillBranch("ZGJ_photon_mass", photons[tight_photons[0]].mass)
                self.out.fillBranch("ZGJ_photon_index", tight_photons[0])
                self.out.fillBranch("ZGJ_photon_vidNestedWPBitmap", photons[tight_photons[0]].vidNestedWPBitmap)
                self.out.fillBranch("ZGJ_photon_pfRelIso03_chg", photons[tight_photons[0]].pfRelIso03_chg)
                self.out.fillBranch("ZGJ_photon_sieie", photons[tight_photons[0]].sieie)
                if hasattr(photons[tight_photons[0]], "genPartFlav"):
                    self.out.fillBranch("ZGJ_photon_genPartFlav", photons[tight_photons[0]].genPartFlav)
                if hasattr(electrons[tight_electrons[0]], "genPartFlav"):
                    self.out.fillBranch("ZGJ_lepton1_genPartFlav", electrons[tight_electrons[0]].genPartFlav)
                    self.out.fillBranch("ZGJ_lepton2_genPartFlav", electrons[tight_electrons[1]].genPartFlav)
                return True

            elif len(tight_muons) == 2:
                dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                m_lla = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + photons[tight_photons[0]].p4()).M()
                dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                m_lla = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + photons[tight_photons[0]].p4()).M()
                self.out.fillBranch("channel_mark", 32)
                self.out.fillBranch("region_mark", region_mark)
                self.out.fillBranch("ZGJ_lepton1_pt", muons[tight_muons[0]].pt)
                self.out.fillBranch("ZGJ_lepton1_eta", muons[tight_muons[0]].eta)
                self.out.fillBranch("ZGJ_lepton1_phi", muons[tight_muons[0]].phi)
                self.out.fillBranch("ZGJ_lepton1_mass", muons[tight_muons[0]].mass)
                self.out.fillBranch("ZGJ_lepton1_index", tight_muons[0])
                self.out.fillBranch("ZGJ_lepton2_pt", muons[tight_muons[1]].pt)
                self.out.fillBranch("ZGJ_lepton2_eta", muons[tight_muons[1]].eta)
                self.out.fillBranch("ZGJ_lepton2_phi", muons[tight_muons[1]].phi)
                self.out.fillBranch("ZGJ_lepton2_mass", muons[tight_muons[1]].mass)
                self.out.fillBranch("ZGJ_lepton2_index", tight_muons[1])
                self.out.fillBranch("ZGJ_dileptonmass", dileptonmass)
                self.out.fillBranch("ZGJ_mlla", m_lla)
                self.out.fillBranch("ZGJ_photon_pt", photons[tight_photons[0]].pt)
                self.out.fillBranch("ZGJ_photon_eta", photons[tight_photons[0]].eta)
                self.out.fillBranch("ZGJ_photon_phi", photons[tight_photons[0]].phi)
                self.out.fillBranch("ZGJ_photon_mass", photons[tight_photons[0]].mass)
                self.out.fillBranch("ZGJ_photon_index", tight_photons[0])
                self.out.fillBranch("ZGJ_photon_vidNestedWPBitmap", photons[tight_photons[0]].vidNestedWPBitmap)
                self.out.fillBranch("ZGJ_photon_pfRelIso03_chg", photons[tight_photons[0]].pfRelIso03_chg)
                self.out.fillBranch("ZGJ_photon_sieie", photons[tight_photons[0]].sieie)
                if hasattr(photons[tight_photons[0]], "genPartFlav"):
                    self.out.fillBranch("ZGJ_photon_genPartFlav", photons[tight_photons[0]].genPartFlav)
                if hasattr(muons[tight_muons[0]], "genPartFlav"):
                    self.out.fillBranch("ZGJ_lepton1_genPartFlav", muons[tight_muons[0]].genPartFlav)
                    self.out.fillBranch("ZGJ_lepton2_genPartFlav", muons[tight_muons[1]].genPartFlav)
                return True


        # ttZ ttW Control Region
        # others are same with Signal Region except:
        # no |m(lz1,lz2,a)+m(lz1,lz2)| requirement
        # no photon requirement
        # |m(lz1,lz2)-mz| > 15
        # nBjets > 0 

        # WZG Signal Region
        # MET > 30
        # 3 leptons with an OSSF lepton pair, mll cloest to mz as z leptons
        # loose lepton veto
        # pt(lz1) > 25, pt(lz2) > 15, pt(lw) > 25
        # |m(lz1,lz2)-mz| <= 15
        # >=1 tight photon
        # |m(lz1,lz2,a)+m(lz1,lz2)| >= 182 !!abandoned!!
        # m(lz1,lz2) > 4
        # m(lll) > 100
        # Bjets veto

        # 3 leptons situation
        # (fff + fft + ftt + ttt)
        if ntightandfakeleptons == 3:
            
            # ttt plus nf, if n=0 region 1 else veto
            if ntightleptons == 3:
                if len(fake_muons) + len(fake_electrons) + len(veto_muons) + len(veto_electrons) != 0:
                    return False

            # Check if it is fff/fft/ftt set it as region 2, elif ttt set it as region 1:
            if len(fake_muons) + len(fake_electrons) != 0:
                region_mark = 2
                # Merge tight and fake for convenience
                tight_muons = tight_muons + fake_muons
                tight_muons.sort(key=lambda x: muons[x].pt, reverse=True)
                tight_electrons = tight_electrons + fake_electrons
                tight_electrons.sort(key=lambda x: electrons[x].pt, reverse=True)

            # check if fake photons exist, else = region 1
            if len(fake_photons) != 0:
                if len(tight_photons) == 0:
                    # no tight photons in fff/fft/ftt: region 2
                    if region_mark == 2:
                        pass
                    # (ttt) or (ttt plus nf) with only fake photons = region 3
                    # Merge tight and fake for convenience
                    else:
                        region_mark = 3
                        tight_photons = tight_photons + fake_photons
                        tight_photons.sort(key=lambda x: photons[x].pt, reverse=True)
                elif photons[tight_photons[0]].pt < photons[fake_photons[0]].pt:
                    # fff/fft/ftt with tight photons included = region 2
                    if region_mark == 2:
                        pass
                    # *FIXME* ttt with leading fake photon still = region 1
                    # TBD, a potential overlap problem here
                    else:
                        pass

            dileptonmass = float('inf')
            trileptonmass = float('inf')
            m_lla = -float('inf')
            # emumu
            if len(tight_muons)==2 and len(tight_electrons)==1:  # emumu channel 
                if muons[tight_muons[0]].pdgId == -muons[tight_muons[1]].pdgId:

                    if muons[tight_muons[0]].pt < 25:
                        return False
                    if electrons[tight_electrons[0]].pt < 25:
                        return False

                    dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                    trileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + electrons[tight_electrons[0]].p4()).M()
                    if len(tight_photons) > 0:
                        m_lla = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + photons[tight_photons[0]].p4()).M()

                if (dileptonmass <= 4): 
                    return False
                
                temp_wl1_p4 = electrons[tight_electrons[0]].p4()
                temp_wl1_index = tight_electrons[0]
                temp_zl1_p4 = muons[tight_muons[0]].p4()
                temp_zl1_index = tight_muons[0]
                temp_zl1_p4.SetPtEtaPhiM(event.Muon_corrected_pt[0], temp_zl1_p4.Eta(), temp_zl1_p4.Phi(), temp_zl1_p4.M())
                temp_zl2_p4 = muons[tight_muons[1]].p4()
                temp_zl2_index = tight_muons[1]
                temp_zl2_p4.SetPtEtaPhiM(event.Muon_corrected_pt[1], temp_zl2_p4.Eta(), temp_zl2_p4.Phi(), temp_zl2_p4.M())
                if hasattr(muons[tight_muons[0]],"genPartFlav"):
                    temp_wl1_genPartFlav = electrons[tight_electrons[0]].genPartFlav
                    temp_zl1_genPartFlav = muons[tight_muons[0]].genPartFlav
                    temp_zl2_genPartFlav = muons[tight_muons[0]].genPartFlav
                channel = 1


            # muee
            if len(tight_muons)==1 and len(tight_electrons)==2:
                if electrons[tight_electrons[0]].pdgId == -electrons[tight_electrons[1]].pdgId:

                    if muons[tight_muons[0]].pt < 25:
                        return False
                    if electrons[tight_electrons[0]].pt < 25:
                        return False

                    dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
                    trileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4() + muons[tight_muons[0]].p4()).M()
                    if len(tight_photons) > 0:
                        m_lla = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4() + photons[tight_photons[0]].p4()).M()

                if (dileptonmass <= 4): 
                    return False
                
                temp_wl1_p4 = muons[tight_muons[0]].p4()
                temp_wl1_index = tight_muons[0]
                temp_wl1_p4.SetPtEtaPhiM(event.Muon_corrected_pt[0], temp_wl1_p4.Eta(), temp_wl1_p4.Phi(), temp_wl1_p4.M())
                temp_zl1_p4 = electrons[tight_electrons[0]].p4()
                temp_zl1_index = tight_electrons[0]
                temp_zl2_p4 = electrons[tight_electrons[1]].p4()
                temp_zl2_index= tight_electrons[1]
                if hasattr(muons[tight_muons[0]],"genPartFlav"):
                    temp_wl1_genPartFlav = muons[tight_muons[0]].genPartFlav
                    temp_zl1_genPartFlav = electrons[tight_electrons[0]].genPartFlav
                    temp_zl2_genPartFlav = electrons[tight_electrons[0]].genPartFlav
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
                trileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4() + electrons[tight_electrons[2]].p4()).M()
                if (mll13 <= 4) or (mll23 <= 4):
                    return False
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

                if len(tight_photons) > 0:
                    m_lla = (electrons[tight_electrons[1]].p4() + electrons[tight_electrons[2]].p4() + photons[tight_photons[0]].p4()).M()

                temp_wl1_p4 = electrons[tight_electrons[0]].p4()
                temp_wl1_index = tight_electrons[0]
                temp_zl1_p4 = electrons[tight_electrons[1]].p4()
                temp_zl1_index = tight_electrons[1]
                temp_zl2_p4 = electrons[tight_electrons[2]].p4()
                temp_zl2_index = tight_electrons[2]
                if hasattr(electrons[tight_electrons[0]],"genPartFlav"):
                    temp_wl1_genPartFlav = electrons[tight_electrons[0]].genPartFlav
                    temp_zl1_genPartFlav = electrons[tight_electrons[1]].genPartFlav
                    temp_zl2_genPartFlav = electrons[tight_electrons[2]].genPartFlav

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
                trileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + muons[tight_muons[2]].p4()).M()
                if (mll13 <= 4) or (mll23 <= 4):
                    return False
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
                if (muons[tight_muons[1]].pt < 25) and (muons[tight_muons[2]].pt < 25):
                    return False
                if len(tight_photons) > 0:
                    m_lla = (muons[tight_muons[1]].p4() + muons[tight_muons[2]].p4() + photons[tight_photons[0]].p4()).M()

                temp_wl1_p4 = muons[tight_muons[0]].p4()
                temp_wl1_index = tight_muons[0]
                temp_wl1_p4.SetPtEtaPhiM(event.Muon_corrected_pt[0], temp_wl1_p4.Eta(), temp_wl1_p4.Phi(), temp_wl1_p4.M())
                temp_zl1_p4 = muons[tight_muons[1]].p4()
                temp_zl1_index = tight_muons[1]
                temp_zl1_p4.SetPtEtaPhiM(event.Muon_corrected_pt[1], temp_zl1_p4.Eta(), temp_zl1_p4.Phi(), temp_zl1_p4.M())
                temp_zl2_p4 = muons[tight_muons[2]].p4()
                temp_zl2_index = tight_muons[2]
                temp_zl2_p4.SetPtEtaPhiM(event.Muon_corrected_pt[2], temp_zl2_p4.Eta(), temp_zl2_p4.Phi(), temp_zl2_p4.M())
                if hasattr(muons[tight_muons[0]],"genPartFlav"):
                    temp_wl1_genPartFlav = muons[tight_muons[0]].genPartFlav
                    temp_zl1_genPartFlav = muons[tight_muons[1]].genPartFlav
                    temp_zl2_genPartFlav = muons[tight_muons[2]].genPartFlav

                channel = 4
            
            if len(tight_bjets) > 0:

                if len(tight_photons) > 0:

                    dr_wla = deltaR(temp_wl1_p4.Eta(),temp_wl1_p4.Phi(),photons[tight_photons[0]].eta,photons[tight_photons[0]].phi)
                    dr_zl1a = deltaR(temp_zl1_p4.Eta(),temp_zl1_p4.Phi(),photons[tight_photons[0]].eta,photons[tight_photons[0]].phi)
                    dr_zl2a = deltaR(temp_zl2_p4.Eta(),temp_zl2_p4.Phi(),photons[tight_photons[0]].eta,photons[tight_photons[0]].phi)
                    mwa = (temp_wl1_p4 + photons[tight_photons[0]].p4()).M()

                    channel += 20
                    self.out.fillBranch("channel_mark", channel)
                    self.out.fillBranch("region_mark", region_mark)
                    # l1: w, l2: zl1, l3: zl2
                    self.out.fillBranch("ttG_lepton1_pt", temp_wl1_p4.Pt())
                    self.out.fillBranch("ttG_lepton1_eta", temp_wl1_p4.Eta())
                    self.out.fillBranch("ttG_lepton1_phi", temp_wl1_p4.Phi())
                    self.out.fillBranch("ttG_lepton1_mass", temp_wl1_p4.M())
                    self.out.fillBranch("ttG_lepton1_index", temp_wl1_index)
                    self.out.fillBranch("ttG_lepton2_pt", temp_zl1_p4.Pt())
                    self.out.fillBranch("ttG_lepton2_eta", temp_zl1_p4.Eta())
                    self.out.fillBranch("ttG_lepton2_phi", temp_zl1_p4.Phi())
                    self.out.fillBranch("ttG_lepton2_mass", temp_zl1_p4.M())
                    self.out.fillBranch("ttG_lepton2_index", temp_zl1_index)
                    self.out.fillBranch("ttG_lepton3_pt", temp_zl2_p4.Pt())
                    self.out.fillBranch("ttG_lepton3_eta", temp_zl2_p4.Eta())
                    self.out.fillBranch("ttG_lepton3_phi", temp_zl2_p4.Phi())
                    self.out.fillBranch("ttG_lepton3_mass", temp_zl2_p4.M())
                    self.out.fillBranch("ttG_lepton3_index", temp_zl2_index)
                    self.out.fillBranch("ttG_photon_pt", photons[tight_photons[0]].pt)
                    self.out.fillBranch("ttG_photon_eta", photons[tight_photons[0]].eta)
                    self.out.fillBranch("ttG_photon_phi", photons[tight_photons[0]].phi)
                    self.out.fillBranch("ttG_photon_mass", photons[tight_photons[0]].mass)
                    self.out.fillBranch("ttG_photon_mass", photons[tight_photons[0]].mass)
                    self.out.fillBranch("ttG_photon_index", tight_photons[0])
                    self.out.fillBranch("ttG_photon_vidNestedWPBitmap", photons[tight_photons[0]].vidNestedWPBitmap)
                    self.out.fillBranch("ttG_photon_pfRelIso03_chg", photons[tight_photons[0]].pfRelIso03_chg)
                    self.out.fillBranch("ttG_photon_sieie", photons[tight_photons[0]].sieie)
                    if hasattr(photons[tight_photons[0]], "genPartFlav"):
                        self.out.fillBranch("ttG_photon_genPartFlav", photons[tight_photons[0]].genPartFlav)
                    if 'temp_wl1_genPartFlav' in locals():
                        self.out.fillBranch("ttG_lepton1_genPartFlav", temp_wl1_genPartFlav)
                        self.out.fillBranch("ttG_lepton2_genPartFlav", temp_zl1_genPartFlav)
                        self.out.fillBranch("ttG_lepton3_genPartFlav", temp_zl2_genPartFlav)
                    self.out.fillBranch("ttG_dileptonmass", dileptonmass)
                    self.out.fillBranch("ttG_trileptonmass", trileptonmass)
                    self.out.fillBranch("ttG_mlla", m_lla)
                    self.out.fillBranch("ttG_MET", MET)
                    self.out.fillBranch("dr_wla", dr_wla)
                    self.out.fillBranch("dr_zl1a", dr_zl1a)
                    self.out.fillBranch("dr_zl2a", dr_zl2a)
                    self.out.fillBranch("mwa", mwa)
                    return True

                else:
                    channel += 10
                    self.out.fillBranch("channel_mark", channel)
                    self.out.fillBranch("region_mark", region_mark)
                    # l1: w, l2: zl1, l3: zl2
                    self.out.fillBranch("ttZ_lepton1_pt", temp_wl1_p4.Pt())
                    self.out.fillBranch("ttZ_lepton1_eta", temp_wl1_p4.Eta())
                    self.out.fillBranch("ttZ_lepton1_phi", temp_wl1_p4.Phi())
                    self.out.fillBranch("ttZ_lepton1_mass", temp_wl1_p4.M())
                    self.out.fillBranch("ttZ_lepton1_index", temp_wl1_index)
                    self.out.fillBranch("ttZ_lepton2_pt", temp_zl1_p4.Pt())
                    self.out.fillBranch("ttZ_lepton2_eta", temp_zl1_p4.Eta())
                    self.out.fillBranch("ttZ_lepton2_phi", temp_zl1_p4.Phi())
                    self.out.fillBranch("ttZ_lepton2_mass", temp_zl1_p4.M())
                    self.out.fillBranch("ttZ_lepton2_index", temp_zl1_index)
                    self.out.fillBranch("ttZ_lepton3_pt", temp_zl2_p4.Pt())
                    self.out.fillBranch("ttZ_lepton3_eta", temp_zl2_p4.Eta())
                    self.out.fillBranch("ttZ_lepton3_phi", temp_zl2_p4.Phi())
                    self.out.fillBranch("ttZ_lepton3_mass", temp_zl2_p4.M())
                    self.out.fillBranch("ttZ_lepton3_index", temp_zl2_index)
                    if 'temp_wl1_genPartFlav' in locals():
                        self.out.fillBranch("ttZ_lepton1_genPartFlav", temp_wl1_genPartFlav)
                        self.out.fillBranch("ttZ_lepton2_genPartFlav", temp_zl1_genPartFlav)
                        self.out.fillBranch("ttZ_lepton3_genPartFlav", temp_zl2_genPartFlav)
                    self.out.fillBranch("ttZ_dileptonmass", dileptonmass)
                    self.out.fillBranch("ttZ_trileptonmass", trileptonmass)
                    self.out.fillBranch("ttZ_MET", MET)
                    return True
            
            elif len(tight_bjets) == 0:

                if len(tight_photons) == 0:
                    return False

                dr_wla = deltaR(temp_wl1_p4.Eta(),temp_wl1_p4.Phi(),photons[tight_photons[0]].eta,photons[tight_photons[0]].phi)
                dr_zl1a = deltaR(temp_zl1_p4.Eta(),temp_zl1_p4.Phi(),photons[tight_photons[0]].eta,photons[tight_photons[0]].phi)
                dr_zl2a = deltaR(temp_zl2_p4.Eta(),temp_zl2_p4.Phi(),photons[tight_photons[0]].eta,photons[tight_photons[0]].phi)
                mwa = (temp_wl1_p4 + photons[tight_photons[0]].p4()).M()

                self.out.fillBranch("channel_mark", channel)
                self.out.fillBranch("region_mark", region_mark)
                # l1: w, l2: zl1, l3: zl2
                self.out.fillBranch("WZG_lepton1_pt", temp_wl1_p4.Pt())
                self.out.fillBranch("WZG_lepton1_eta", temp_wl1_p4.Eta())
                self.out.fillBranch("WZG_lepton1_phi", temp_wl1_p4.Phi())
                self.out.fillBranch("WZG_lepton1_mass", temp_wl1_p4.M())
                self.out.fillBranch("WZG_lepton1_index", temp_wl1_index)
                self.out.fillBranch("WZG_lepton2_pt", temp_zl1_p4.Pt())
                self.out.fillBranch("WZG_lepton2_eta", temp_zl1_p4.Eta())
                self.out.fillBranch("WZG_lepton2_phi", temp_zl1_p4.Phi())
                self.out.fillBranch("WZG_lepton2_mass", temp_zl1_p4.M())
                self.out.fillBranch("WZG_lepton2_index", temp_zl1_index)
                self.out.fillBranch("WZG_lepton3_pt", temp_zl2_p4.Pt())
                self.out.fillBranch("WZG_lepton3_eta", temp_zl2_p4.Eta())
                self.out.fillBranch("WZG_lepton3_phi", temp_zl2_p4.Phi())
                self.out.fillBranch("WZG_lepton3_mass", temp_zl2_p4.M())
                self.out.fillBranch("WZG_lepton3_index", temp_zl2_index)
                self.out.fillBranch("WZG_photon_pt", photons[tight_photons[0]].pt)
                self.out.fillBranch("WZG_photon_eta", photons[tight_photons[0]].eta)
                self.out.fillBranch("WZG_photon_phi", photons[tight_photons[0]].phi)
                self.out.fillBranch("WZG_photon_mass", photons[tight_photons[0]].mass)
                self.out.fillBranch("WZG_photon_index", tight_photons[0])
                self.out.fillBranch("WZG_photon_vidNestedWPBitmap", photons[tight_photons[0]].vidNestedWPBitmap)
                self.out.fillBranch("WZG_photon_pfRelIso03_chg", photons[tight_photons[0]].pfRelIso03_chg)
                self.out.fillBranch("WZG_photon_sieie", photons[tight_photons[0]].sieie)
                if hasattr(photons[tight_photons[0]], "genPartFlav"):
                    self.out.fillBranch("WZG_photon_genPartFlav", photons[tight_photons[0]].genPartFlav)
                if 'temp_wl1_genPartFlav' in locals():
                    self.out.fillBranch("WZG_lepton1_genPartFlav", temp_wl1_genPartFlav)
                    self.out.fillBranch("WZG_lepton2_genPartFlav", temp_zl1_genPartFlav)
                    self.out.fillBranch("WZG_lepton3_genPartFlav", temp_zl2_genPartFlav)
                self.out.fillBranch("WZG_dileptonmass", dileptonmass)
                self.out.fillBranch("WZG_trileptonmass", trileptonmass)
                self.out.fillBranch("WZG_mlla", m_lla)
                self.out.fillBranch("WZG_MET", MET)
                self.out.fillBranch("dr_wla", dr_wla)
                self.out.fillBranch("dr_zl1a", dr_zl1a)
                self.out.fillBranch("dr_zl2a", dr_zl2a)
                self.out.fillBranch("mwa", mwa)
                return True


        # ZZ leptonic Control Region
        # 4 tight leptons, 2 OSSF lepton pairs, mll cloest to mz as z(l1 l2) leptons.
        # |m(zl1,zl2)-mz| <= 15
        # min mll > 4
        # >=0 tight photon
        # Bjets veto

        # 4 leptons situation
        # (ffff + ffft + fftt + fttt + tttt)
        if ntightandfakeleptons == 4:
            
            # tttt plus nf, if n=0 region 1 else veto
            if ntightleptons == 4:
                if len(fake_muons) + len(fake_electrons) + len(veto_muons) + len(veto_electrons) != 0:
                    return False

            # Check if it is ffff/ffft/fftt/fttt set it as region 2, elif ttt set it as region 1:
            if len(fake_muons) + len(fake_electrons) != 0:
                region_mark = 2
                # Merge tight and fake for convenience
                tight_muons = tight_muons + fake_muons
                tight_muons.sort(key=lambda x: muons[x].pt, reverse=True)
                tight_electrons = tight_electrons + fake_electrons
                tight_electrons.sort(key=lambda x: electrons[x].pt, reverse=True)

        # lepton is ordered with z1(ll) z2(ll)
        if len(tight_electrons) + len(tight_muons) == 4:

            if len(tight_bjets) > 0:
                return False

            if len(tight_electrons) == 2 and len(tight_muons) == 2:
                z_pair_mark = -99
                # 1: ee pair as z pair
                # 2: mm pair as z pair
                if (muons[tight_muons[0]].charge == muons[tight_muons[1]].charge) or (electrons[tight_electrons[0]].charge == electrons[tight_electrons[1]].charge):
                    return False
                dileptonmass_zm = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()
                dileptonmass_ze = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()
                if dileptonmass_ze <= 4 or dileptonmass_zm <= 4:
                    return False
                if abs(dileptonmass_ze-91.188) < abs(dileptonmass_zm-91.188):
                    z_pair_mark = 1
                    mllz1 = dileptonmass_ze
                    mllz2 = dileptonmass_zm
                    trileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4() + muons[tight_muons[0]].p4()).M()
                else:
                    z_pair_mark = 2
                    mllz1 = dileptonmass_zm
                    mllz2 = dileptonmass_ze
                    trileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4() + electrons[tight_electrons[0]].p4()).M()
                if (abs(mllz1-91.188)>15):
                    return False
                if z_pair_mark == 1:
                    self.out.fillBranch("channel_mark", 5)
                    self.out.fillBranch("region_mark", region_mark)
                    self.out.fillBranch("ZZ_lepton1_pt", electrons[tight_electrons[0]].pt)
                    self.out.fillBranch("ZZ_lepton1_eta", electrons[tight_electrons[0]].eta)
                    self.out.fillBranch("ZZ_lepton1_phi", electrons[tight_electrons[0]].phi)
                    self.out.fillBranch("ZZ_lepton1_mass", electrons[tight_electrons[0]].mass)
                    self.out.fillBranch("ZZ_lepton1_index", tight_electrons[0])
                    self.out.fillBranch("ZZ_lepton2_pt", electrons[tight_electrons[1]].pt)
                    self.out.fillBranch("ZZ_lepton2_eta", electrons[tight_electrons[1]].eta)
                    self.out.fillBranch("ZZ_lepton2_phi", electrons[tight_electrons[1]].phi)
                    self.out.fillBranch("ZZ_lepton2_mass", electrons[tight_electrons[1]].mass)
                    self.out.fillBranch("ZZ_lepton2_index", tight_electrons[1])
                    self.out.fillBranch("ZZ_lepton3_pt", event.Muon_corrected_pt[tight_muons[0]])
                    self.out.fillBranch("ZZ_lepton3_eta", muons[tight_muons[0]].eta)
                    self.out.fillBranch("ZZ_lepton3_phi", muons[tight_muons[0]].phi)
                    self.out.fillBranch("ZZ_lepton3_mass", muons[tight_muons[0]].mass)
                    self.out.fillBranch("ZZ_lepton3_index", tight_muons[0])
                    self.out.fillBranch("ZZ_lepton4_pt", event.Muon_corrected_pt[tight_muons[1]])
                    self.out.fillBranch("ZZ_lepton4_eta", muons[tight_muons[1]].eta)
                    self.out.fillBranch("ZZ_lepton4_phi", muons[tight_muons[1]].phi)
                    self.out.fillBranch("ZZ_lepton4_mass", muons[tight_muons[1]].mass)
                    self.out.fillBranch("ZZ_lepton4_index", tight_muons[1])
                    if hasattr(muons[tight_muons[0]],"genPartFlav"):
                        self.out.fillBranch("ZZ_lepton1_genPartFlav", electrons[tight_electrons[0]].genPartFlav)
                        self.out.fillBranch("ZZ_lepton2_genPartFlav", electrons[tight_electrons[1]].genPartFlav)
                        self.out.fillBranch("ZZ_lepton3_genPartFlav", muons[tight_muons[0]].genPartFlav)
                        self.out.fillBranch("ZZ_lepton4_genPartFlav", muons[tight_muons[1]].genPartFlav)
                if z_pair_mark == 2:
                    self.out.fillBranch("channel_mark", 6)
                    self.out.fillBranch("region_mark", region_mark)
                    self.out.fillBranch("ZZ_lepton1_pt", event.Muon_corrected_pt[tight_muons[0]])
                    self.out.fillBranch("ZZ_lepton1_eta", muons[tight_muons[0]].eta)
                    self.out.fillBranch("ZZ_lepton1_phi", muons[tight_muons[0]].phi)
                    self.out.fillBranch("ZZ_lepton1_mass", muons[tight_muons[0]].mass)
                    self.out.fillBranch("ZZ_lepton1_index", tight_muons[0])
                    self.out.fillBranch("ZZ_lepton2_pt", event.Muon_corrected_pt[tight_muons[1]])
                    self.out.fillBranch("ZZ_lepton2_eta", muons[tight_muons[1]].eta)
                    self.out.fillBranch("ZZ_lepton2_phi", muons[tight_muons[1]].phi)
                    self.out.fillBranch("ZZ_lepton2_mass", muons[tight_muons[1]].mass)
                    self.out.fillBranch("ZZ_lepton2_index", tight_muons[1])
                    self.out.fillBranch("ZZ_lepton3_pt", electrons[tight_electrons[0]].pt)
                    self.out.fillBranch("ZZ_lepton3_eta", electrons[tight_electrons[0]].eta)
                    self.out.fillBranch("ZZ_lepton3_phi", electrons[tight_electrons[0]].phi)
                    self.out.fillBranch("ZZ_lepton3_mass", electrons[tight_electrons[0]].mass)
                    self.out.fillBranch("ZZ_lepton3_index", tight_electrons[0])
                    self.out.fillBranch("ZZ_lepton4_pt", electrons[tight_electrons[1]].pt)
                    self.out.fillBranch("ZZ_lepton4_eta", electrons[tight_electrons[1]].eta)
                    self.out.fillBranch("ZZ_lepton4_phi", electrons[tight_electrons[1]].phi)
                    self.out.fillBranch("ZZ_lepton4_mass", electrons[tight_electrons[1]].mass)
                    self.out.fillBranch("ZZ_lepton4_index", tight_electrons[1])
                    if hasattr(muons[tight_muons[0]],"genPartFlav"):
                        self.out.fillBranch("ZZ_lepton1_genPartFlav", muons[tight_muons[0]].genPartFlav)
                        self.out.fillBranch("ZZ_lepton2_genPartFlav", muons[tight_muons[1]].genPartFlav)
                        self.out.fillBranch("ZZ_lepton3_genPartFlav", electrons[tight_electrons[0]].genPartFlav)
                        self.out.fillBranch("ZZ_lepton4_genPartFlav", electrons[tight_electrons[1]].genPartFlav)
                    
                self.out.fillBranch("ZZ_mllz1", mllz1)
                self.out.fillBranch("ZZ_mllz2", mllz2)
                self.out.fillBranch("ZZ_trileptonmass", trileptonmass)
                self.out.fillBranch("ZZ_MET", MET)
                return True

            elif len(tight_electrons) == 4:

                charge_list = []
                for i in range(0,len(tight_electrons)):
                    charge_list.append(electrons[tight_electrons[i]].charge)
                if (charge_list.count(1)!=2) or (charge_list.count(-1)!=2):
                    return False

                dileptonmass_temp = []
                for i in range(0,len(tight_electrons)):
                    for j in range(i+1, len(tight_electrons)):
                        if electrons[tight_electrons[i]].charge == electrons[tight_electrons[j]].charge:
                            dileptonmass_temp.append(float('inf'))
                        else:
                            dileptonmass_temp.append((electrons[tight_electrons[i]].p4() + electrons[tight_electrons[j]].p4()).M())

                if min(dileptonmass_temp) <= 4:
                    return False

                abs_mll_mz = [abs(x-91.188) for x in dileptonmass_temp]
                if min(abs_mll_mz) > 15:
                    return False
                
                l1_index, l2_index, l3_index, l4_index = self.ZZ_GetLepIndex(abs_mll_mz)
                self.out.fillBranch("channel_mark", 7)
                self.out.fillBranch("region_mark", region_mark)
                self.out.fillBranch("ZZ_lepton1_pt", electrons[tight_electrons[l1_index]].pt)
                self.out.fillBranch("ZZ_lepton1_eta", electrons[tight_electrons[l1_index]].eta)
                self.out.fillBranch("ZZ_lepton1_phi", electrons[tight_electrons[l1_index]].phi)
                self.out.fillBranch("ZZ_lepton1_mass", electrons[tight_electrons[l1_index]].mass)
                self.out.fillBranch("ZZ_lepton1_index", tight_electrons[l1_index])
                self.out.fillBranch("ZZ_lepton2_pt", electrons[tight_electrons[l2_index]].pt)
                self.out.fillBranch("ZZ_lepton2_eta", electrons[tight_electrons[l2_index]].eta)
                self.out.fillBranch("ZZ_lepton2_phi", electrons[tight_electrons[l2_index]].phi)
                self.out.fillBranch("ZZ_lepton2_mass", electrons[tight_electrons[l2_index]].mass)
                self.out.fillBranch("ZZ_lepton2_index", tight_electrons[l2_index])
                self.out.fillBranch("ZZ_lepton3_pt", electrons[tight_electrons[l3_index]].pt)
                self.out.fillBranch("ZZ_lepton3_eta", electrons[tight_electrons[l3_index]].eta)
                self.out.fillBranch("ZZ_lepton3_phi", electrons[tight_electrons[l3_index]].phi)
                self.out.fillBranch("ZZ_lepton3_mass", electrons[tight_electrons[l3_index]].mass)
                self.out.fillBranch("ZZ_lepton3_index", tight_electrons[l3_index])
                self.out.fillBranch("ZZ_lepton4_pt", electrons[tight_electrons[l4_index]].pt)
                self.out.fillBranch("ZZ_lepton4_eta", electrons[tight_electrons[l4_index]].eta)
                self.out.fillBranch("ZZ_lepton4_phi", electrons[tight_electrons[l4_index]].phi)
                self.out.fillBranch("ZZ_lepton4_mass", electrons[tight_electrons[l4_index]].mass)
                self.out.fillBranch("ZZ_lepton4_index", tight_electrons[l4_index])
                if hasattr(electrons[tight_electrons[0]],"genPartFlav"):
                    self.out.fillBranch("ZZ_lepton1_genPartFlav", electrons[tight_electrons[l1_index]].genPartFlav)
                    self.out.fillBranch("ZZ_lepton2_genPartFlav", electrons[tight_electrons[l2_index]].genPartFlav)
                    self.out.fillBranch("ZZ_lepton3_genPartFlav", electrons[tight_electrons[l3_index]].genPartFlav)
                    self.out.fillBranch("ZZ_lepton4_genPartFlav", electrons[tight_electrons[l4_index]].genPartFlav)
                    
                self.out.fillBranch("ZZ_mllz1", dileptonmass_temp[abs_mll_mz.index(min(abs_mll_mz))])
                self.out.fillBranch("ZZ_mllz2", (electrons[tight_electrons[l3_index]].p4() + electrons[tight_electrons[l4_index]].p4()).M())
                self.out.fillBranch("ZZ_trileptonmass", (electrons[tight_electrons[l1_index]].p4() + electrons[tight_electrons[l2_index]].p4() + electrons[tight_electrons[l3_index]].p4()).M())
                self.out.fillBranch("ZZ_MET", MET)
                return True


            elif len(tight_muons) == 4:

                charge_list = []
                for i in range(0,len(tight_muons)):
                    charge_list.append(muons[tight_muons[i]].charge)
                if (charge_list.count(1)!=2) or (charge_list.count(-1)!=2):
                    return False

                dileptonmass_temp = []
                for i in range(0,len(tight_muons)):
                    for j in range(i+1, len(tight_muons)):
                        if muons[tight_muons[i]].charge == muons[tight_muons[j]].charge:
                            dileptonmass_temp.append(float('inf'))
                        else:
                            dileptonmass_temp.append((muons[tight_muons[i]].p4() + muons[tight_muons[j]].p4()).M())

                if min(dileptonmass_temp) <= 4:
                    return False

                abs_mll_mz = [abs(x-91.188) for x in dileptonmass_temp]
                if min(abs_mll_mz) > 15:
                    return False
                
                l1_index, l2_index, l3_index, l4_index = self.ZZ_GetLepIndex(abs_mll_mz)
                self.out.fillBranch("channel_mark", 8)
                self.out.fillBranch("region_mark", region_mark)
                self.out.fillBranch("ZZ_lepton1_pt", muons[tight_muons[l1_index]].pt)
                self.out.fillBranch("ZZ_lepton1_eta", muons[tight_muons[l1_index]].eta)
                self.out.fillBranch("ZZ_lepton1_phi", muons[tight_muons[l1_index]].phi)
                self.out.fillBranch("ZZ_lepton1_mass", muons[tight_muons[l1_index]].mass)
                self.out.fillBranch("ZZ_lepton1_index", tight_muons[l1_index])
                self.out.fillBranch("ZZ_lepton2_pt", muons[tight_muons[l2_index]].pt)
                self.out.fillBranch("ZZ_lepton2_eta", muons[tight_muons[l2_index]].eta)
                self.out.fillBranch("ZZ_lepton2_phi", muons[tight_muons[l2_index]].phi)
                self.out.fillBranch("ZZ_lepton2_mass", muons[tight_muons[l2_index]].mass)
                self.out.fillBranch("ZZ_lepton2_index", tight_muons[l2_index])
                self.out.fillBranch("ZZ_lepton3_pt", muons[tight_muons[l3_index]].pt)
                self.out.fillBranch("ZZ_lepton3_eta", muons[tight_muons[l3_index]].eta)
                self.out.fillBranch("ZZ_lepton3_phi", muons[tight_muons[l3_index]].phi)
                self.out.fillBranch("ZZ_lepton3_mass", muons[tight_muons[l3_index]].mass)
                self.out.fillBranch("ZZ_lepton3_index", tight_muons[l3_index])
                self.out.fillBranch("ZZ_lepton4_pt", muons[tight_muons[l4_index]].pt)
                self.out.fillBranch("ZZ_lepton4_eta", muons[tight_muons[l4_index]].eta)
                self.out.fillBranch("ZZ_lepton4_phi", muons[tight_muons[l4_index]].phi)
                self.out.fillBranch("ZZ_lepton4_mass", muons[tight_muons[l4_index]].mass)
                self.out.fillBranch("ZZ_lepton4_index", tight_muons[l4_index])
                if hasattr(muons[tight_muons[0]],"genPartFlav"):
                    self.out.fillBranch("ZZ_lepton1_genPartFlav", muons[tight_muons[l1_index]].genPartFlav)
                    self.out.fillBranch("ZZ_lepton2_genPartFlav", muons[tight_muons[l2_index]].genPartFlav)
                    self.out.fillBranch("ZZ_lepton3_genPartFlav", muons[tight_muons[l3_index]].genPartFlav)
                    self.out.fillBranch("ZZ_lepton4_genPartFlav", muons[tight_muons[l4_index]].genPartFlav)
                    
                self.out.fillBranch("ZZ_mllz1", dileptonmass_temp[abs_mll_mz.index(min(abs_mll_mz))])
                self.out.fillBranch("ZZ_mllz2", (muons[tight_muons[l3_index]].p4() + muons[tight_muons[l4_index]].p4()).M())
                self.out.fillBranch("ZZ_trileptonmass", (muons[tight_muons[l1_index]].p4() + muons[tight_muons[l2_index]].p4() + muons[tight_muons[l3_index]].p4()).M())
                self.out.fillBranch("ZZ_MET", MET)
                return True

        return False

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

WZG_select_multi_Module = lambda : WZG_multi_Producer()