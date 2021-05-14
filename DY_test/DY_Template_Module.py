import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class DYTestProducer(Module):
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

        self.out.branch("lepton1_pdgId",  "F")
        self.out.branch("lepton1_pt",  "F")
        self.out.branch("lepton1_gen_matching",  "F")
        self.out.branch("lepton1_eta",  "F")
        self.out.branch("lepton1_phi",  "F")

        self.out.branch("lepton2_pdgId",  "F")
        self.out.branch("lepton2_pt",  "F")
        self.out.branch("lepton2_gen_matching",  "F")
        self.out.branch("lepton2_eta",  "F")
        self.out.branch("lepton2_phi",  "F")

        self.out.branch("gen_weight",  "F")
        self.out.branch("dilepton_mass",  "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        # jets = Collection(event, "Jet")
        # photons = Collection(event, "Photon")

        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []

        tight_photons = []

        tight_jets = []

        for i in range(0,len(muons)):

            if muons[i].pt < 10:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            
            elif muons[i].tightId and muons[i].pfRelIso04_all < 0.4:
                loose_but_not_tight_muons.append(i)

        for i in range (0,len(electrons)):

            if electrons[i].pt < 10:
                continue
            
            if abs(electrons[i].eta+ electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):

                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        if len(tight_muons) == 2 and len(loose_but_not_tight_muons) + len(tight_electrons) + len(loose_but_not_tight_electrons) == 0:

            if muons[tight_muons[0]].charge == muons[tight_muons[1]].charge:
                return False

            dileptonmass = (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M()

            self.out.fillBranch("lepton1_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton1_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton1_phi",muons[tight_muons[0]].phi)
            self.out.fillBranch("lepton1_pdgId",muons[tight_muons[0]].pdgId)

            self.out.fillBranch("lepton2_pt",muons[tight_muons[1]].pt)
            self.out.fillBranch("lepton2_eta",muons[tight_muons[1]].eta)
            self.out.fillBranch("lepton2_phi",muons[tight_muons[1]].phi)
            self.out.fillBranch("lepton2_pdgId",muons[tight_muons[1]].pdgId)

            if hasattr(muons[tight_muons[0]],'genPartFlav'):
                self.out.fillBranch("lepton1_gen_matching",muons[tight_muons[0]].genPartFlav)
                self.out.fillBranch("lepton2_gen_matching",muons[tight_muons[1]].genPartFlav)
            else:
                self.out.fillBranch("lepton1_gen_matching",0)                
                self.out.fillBranch("lepton2_gen_matching",0)                

            self.out.fillBranch("dilepton_mass",dileptonmass)

        elif len(tight_electrons) == 2 and len(loose_but_not_tight_muons) + len(tight_muons) + len(loose_but_not_tight_electrons) == 0:

            if electrons[tight_electrons[0]].charge == electrons[tight_electrons[1]].charge:
                return False

            dileptonmass = (electrons[tight_electrons[0]].p4() + electrons[tight_electrons[1]].p4()).M()

            self.out.fillBranch("lepton1_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton1_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton1_phi",electrons[tight_electrons[0]].phi)
            self.out.fillBranch("lepton1_pdgId",electrons[tight_electrons[0]].pdgId)

            self.out.fillBranch("lepton2_pt",electrons[tight_electrons[1]].pt)
            self.out.fillBranch("lepton2_eta",electrons[tight_electrons[1]].eta)
            self.out.fillBranch("lepton2_phi",electrons[tight_electrons[1]].phi)
            self.out.fillBranch("lepton2_pdgId",electrons[tight_electrons[1]].pdgId)

            if hasattr(electrons[tight_electrons[0]],'genPartFlav'):
                self.out.fillBranch("lepton1_gen_matching",electrons[tight_electrons[0]].genPartFlav)
                self.out.fillBranch("lepton2_gen_matching",electrons[tight_electrons[1]].genPartFlav)
            else:
                self.out.fillBranch("lepton1_gen_matching",0)                
                self.out.fillBranch("lepton2_gen_matching",0)                

            self.out.fillBranch("dilepton_mass",dileptonmass)

        else:
            return False

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)

        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        return True

DYTestModule = lambda : DYTestProducer()