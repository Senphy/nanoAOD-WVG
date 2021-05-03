import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class FakeLeptonProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i")
        self.out.branch("lumi",  "i")
        self.out.branch("event",  "l")
        self.out.branch("met",  "F")
        self.out.branch("mt",  "F")
        self.out.branch("jet_pt",  "F")
        self.out.branch("lepton_jet_dr",  "F")
        self.out.branch("hlt",  "i")
        self.out.branch("puppimet",  "F")
        self.out.branch("puppimt",  "F")
        self.out.branch("lepton_pdgid",  "F")
        self.out.branch("lepton_pt",  "F")
        self.out.branch("lepton_gen_matching",  "F")
        self.out.branch("lepton_eta",  "F")
        self.out.branch("lepton_pfRelIso04_all",  "F")
        self.out.branch("lepton_sc_eta",  "F")
        self.out.branch("is_lepton_tight",  "B")
        self.out.branch("gen_weight",  "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        # photons = Collection(event, "Photon")

        tight_muons = []

        fake_rate_denominator_muons = []

        other_loose_muons = []
        
        tight_electrons = []

        fake_rate_denominator_electrons = []
        
        other_loose_electrons = []

        tight_photons = []

        tight_jets = []

        # if event.MET_pt > 20:
        if event.MET_pt > 30:
            return False

        # here the tight muons actually means fake_rate_denominator_muons
        # the numerator is extracted by a different pfRelIso04_all in further analysis
        for i in range(0,len(muons)):

            if muons[i].pt < 10:
            # if muons[i].pt < 20:
                continue

            if abs(muons[i].eta) > 2.4:
            # if abs(muons[i].eta) > 2.5:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.4:
                tight_muons.append(i)

        for i in range (0,len(electrons)):

            if electrons[i].pt < 10:
                continue
            
            if abs(electrons[i].eta+ electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)
                elif electrons[i].cutBased == 1:
                    fake_rate_denominator_electrons.append(i)
                elif electrons[i].cutBased >= 1:
                    other_loose_electrons.append(i)

        if len(tight_muons) == 1 and len(tight_electrons) + len(fake_rate_denominator_electrons) + len(other_loose_electrons) == 0:


            muon_index = tight_muons[0]
            self.out.fillBranch("is_lepton_tight",1)

            found_other_jet = False

            for i in range(0,len(jets)):
                
                if jets[i].pt < 10:
                # if jets[i].pt < 30:
                    continue

                if abs(jets[i].eta) > 2.4:
                    continue

                # for UL samples, jetId=2 means: pass tight ID, fail tightLepVeto
                if not jets[i].jetId & (1 << 1):
                    continue

                if deltaR(muons[muon_index].eta,muons[muon_index].phi,jets[i].eta,jets[i].phi) < 0.5:
                # if deltaR(muons[muon_index].eta,muons[muon_index].phi,jets[i].eta,jets[i].phi) < 0.4:
                    continue

                if not found_other_jet:
                    jet_pt = jets[i].pt
                    lepton_jet_dr = deltaR(muons[muon_index].eta,muons[muon_index].phi,jets[i].eta,jets[i].phi)

                if found_other_jet and jets[i].pt > jet_pt:
                    jet_pt = jets[i].pt
                    lepton_jet_dr = deltaR(muons[muon_index].eta,muons[muon_index].phi,jets[i].eta,jets[i].phi)                        

                found_other_jet = True

            if not found_other_jet:
                return False

            # if muons[muon_index].pt < 26:
            #     return False

            hlt = 0

            # if event.HLT_IsoMu24: # or event.HLT_IsoTkMu24:
            #     hlt += 1 

            # if event.HLT_Mu17_TrkIsoVVL:
            #     hlt += 2

            mt = sqrt(2*muons[muon_index].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[muon_index].phi))) 
            if mt > 20:
                return False

            self.out.fillBranch("mt",sqrt(2*muons[muon_index].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[muon_index].phi))))
            self.out.fillBranch("puppimt",sqrt(2*muons[muon_index].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - muons[muon_index].phi))))

            self.out.fillBranch("lepton_pt",muons[muon_index].pt)
            if hasattr(muons[muon_index],'genPartFlav'):
                self.out.fillBranch("lepton_gen_matching",muons[muon_index].genPartFlav)
            else:
                self.out.fillBranch("lepton_gen_matching",0)                
            self.out.fillBranch("lepton_eta",muons[muon_index].eta)
            self.out.fillBranch("lepton_sc_eta",0)
            self.out.fillBranch("lepton_pdgid",muons[muon_index].pdgId)

            self.out.fillBranch("jet_pt",jet_pt)
            self.out.fillBranch("lepton_jet_dr",lepton_jet_dr)

            self.out.fillBranch("hlt",hlt)

            self.out.fillBranch("lepton_pfRelIso04_all",muons[muon_index].pfRelIso04_all)

        elif len(tight_electrons) + len(fake_rate_denominator_electrons) == 1 and len(tight_muons) + len(other_loose_electrons) == 0:   

            if len(tight_electrons) == 1:
                electron_index = tight_electrons[0]
                self.out.fillBranch("is_lepton_tight",1)

            if len(fake_rate_denominator_electrons) == 1:
                electron_index = fake_rate_denominator_electrons[0]
                self.out.fillBranch("is_lepton_tight",0)

            found_other_jet = False

            for i in range(0,len(jets)):
                
                if jets[i].pt < 10:
                    continue

                if abs(jets[i].eta) > 2.4:
                    continue

                if not jets[i].jetId & (1 << 1):
                    continue

                if deltaR(electrons[electron_index].eta,electrons[electron_index].phi,jets[i].eta,jets[i].phi) < 0.5:
                # if deltaR(electrons[electron_index].eta,electrons[electron_index].phi,jets[i].eta,jets[i].phi) < 0.4:
                    continue

                if not found_other_jet:
                    jet_pt = jets[i].pt
                    lepton_jet_dr = deltaR(electrons[electron_index].eta,electrons[electron_index].phi,jets[i].eta,jets[i].phi)

                if found_other_jet and jets[i].pt > jet_pt:
                    jet_pt = jets[i].pt
                    lepton_jet_dr = deltaR(electrons[electron_index].eta,electrons[electron_index].phi,jets[i].eta,jets[i].phi)                        

                found_other_jet = True

            if not found_other_jet:
                return False

            # if electrons[electron_index].pt < 30:
            #     return False

            hlt = 0

            # if event.HLT_Ele27_WPTight_Gsf:
            #     hlt += 1

            # if event.HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30:
            #     hlt += 2

            mt = sqrt(2*electrons[electron_index].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[electron_index].phi)))
            if mt > 20:
                return False

            self.out.fillBranch("mt",mt)
            self.out.fillBranch("puppimt",sqrt(2*electrons[electron_index].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - electrons[electron_index].phi))))
            self.out.fillBranch("lepton_pt",electrons[electron_index].pt)
            if hasattr(electrons[electron_index],'genPartFlav'):
                self.out.fillBranch("lepton_gen_matching",electrons[electron_index].genPartFlav)
            else:
                self.out.fillBranch("lepton_gen_matching",0)
            self.out.fillBranch("lepton_eta",electrons[electron_index].eta)
            self.out.fillBranch("lepton_sc_eta",electrons[electron_index].eta+electrons[electron_index].deltaEtaSC)
            self.out.fillBranch("lepton_pdgid",electrons[electron_index].pdgId)

            self.out.fillBranch("jet_pt",jet_pt)
            self.out.fillBranch("lepton_jet_dr",lepton_jet_dr)

            self.out.fillBranch("hlt",hlt)
        else:
            return False

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)

        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        return True

FakeLeptonModule = lambda : FakeLeptonProducer()