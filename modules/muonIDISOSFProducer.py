import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import math
import os

class muonIDISOSFProducer(Module):
  def __init__( self , year ):
    self.year = year
    self.id_ = "muon_ID.root"
    self.iso_ = "muon_ISO.root"
    self.SF_location_path = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/data/year%s/" %(os.environ['CMSSW_BASE'], self.year)
    print 'SF location:', self.SF_location_path

  def beginJob(self):
    print 'begin to set Muon ID and ISO SF --->>>'
    print 'start to open SF root file --->>>'
    # init the TH2F
    self.id_loose_th2f= ROOT.TH2F()
    self.id_medium_th2f= ROOT.TH2F()
    self.id_mediumprompt_th2f= ROOT.TH2F()
    self.id_tight_th2f= ROOT.TH2F()
    self.id_soft_th2f= ROOT.TH2F()
    self.id_highpt_th2f= ROOT.TH2F()
    self.id_trkhighpt_th2f= ROOT.TH2F()

    self.iso_looseRelIso_looseID_th2f=ROOT.TH2F()
    self.iso_looseRelIso_mediumID_th2f=ROOT.TH2F()
    self.iso_looseRelIso_mediumpromptID_th2f=ROOT.TH2F()
    self.iso_looseRelIso_tightIDandIPCut_th2f=ROOT.TH2F()
    self.iso_looseRelTkIso_highptIDandIPCut_th2f=ROOT.TH2F()
    self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f=ROOT.TH2F()
    self.iso_tightRelIso_mediumID_th2f=ROOT.TH2F()
    self.iso_tightRelIso_mediumpromptID_th2f=ROOT.TH2F()
    self.iso_tightRelIso_tightIDandIPCut_th2f=ROOT.TH2F()
    self.iso_tightRelTkIso_highptIDandIPCut_th2f=ROOT.TH2F()
    self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f=ROOT.TH2F()
    #Open the SF root file
    self.file_id= ROOT.TFile.Open(self.SF_location_path+self.id_)
    self.file_iso= ROOT.TFile.Open(self.SF_location_path+self.iso_)
    #access to the TH2F
    self.file_id.GetObject('NUM_LooseID_DEN_TrackerMuons_abseta_pt', self.id_loose_th2f)
    self.file_id.GetObject('NUM_MediumID_DEN_TrackerMuons_abseta_pt', self.id_medium_th2f)
    self.file_id.GetObject('NUM_MediumPromptID_DEN_TrackerMuons_abseta_pt', self.id_mediumprompt_th2f)
    self.file_id.GetObject('NUM_TightID_DEN_TrackerMuons_abseta_pt', self.id_tight_th2f)
    self.file_id.GetObject('NUM_SoftID_DEN_TrackerMuons_abseta_pt', self.id_soft_th2f)
    self.file_id.GetObject('NUM_HighPtID_DEN_TrackerMuons_abseta_pt', self.id_highpt_th2f)
    self.file_id.GetObject('NUM_TrkHighPtID_DEN_TrackerMuons_abseta_pt', self.id_trkhighpt_th2f)

    self.file_iso.GetObject('NUM_LooseRelIso_DEN_LooseID_abseta_pt', self.iso_looseRelIso_looseID_th2f)
    self.file_iso.GetObject('NUM_LooseRelIso_DEN_MediumID_abseta_pt', self.iso_looseRelIso_mediumID_th2f)
    self.file_iso.GetObject('NUM_LooseRelIso_DEN_MediumPromptID_abseta_pt',self.iso_looseRelIso_mediumpromptID_th2f)
    self.file_iso.GetObject('NUM_LooseRelIso_DEN_TightIDandIPCut_abseta_pt',self.iso_looseRelIso_tightIDandIPCut_th2f)
    self.file_iso.GetObject('NUM_LooseRelTkIso_DEN_HighPtIDandIPCut_abseta_pt',self.iso_looseRelTkIso_highptIDandIPCut_th2f)
    self.file_iso.GetObject('NUM_LooseRelTkIso_DEN_TrkHighPtIDandIPCut_abseta_pt',self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f)
    self.file_iso.GetObject('NUM_TightRelIso_DEN_MediumID_abseta_pt', self.iso_tightRelIso_mediumID_th2f)
    self.file_iso.GetObject('NUM_TightRelIso_DEN_MediumPromptID_abseta_pt',self.iso_tightRelIso_mediumpromptID_th2f)
    self.file_iso.GetObject('NUM_TightRelIso_DEN_TightIDandIPCut_abseta_pt',self.iso_tightRelIso_tightIDandIPCut_th2f)
    self.file_iso.GetObject('NUM_TightRelTkIso_DEN_HighPtIDandIPCut_abseta_pt',self.iso_tightRelTkIso_highptIDandIPCut_th2f)
    self.file_iso.GetObject('NUM_TightRelTkIso_DEN_TrkHighPtIDandIPCut_abseta_pt',self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f)
    print 'open SF files successfully --->>>'

  def endJob(self):
    print 'close SF root file --->>>'
    self.file_id.Close()
    self.file_iso.Close()
    print 'finish setting Muon ID SF --->>>'
    
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch('Muon_CutBased_LooseID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_LooseID_SFerr','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_MediumID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_MediumID_SFerr','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_MediumPromptID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_MediumPromptID_SFerr','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_TightID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_TightID_SFerr','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_SoftID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_SoftID_SFerr','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_HighPtID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_HighPtID_SFerr','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_TrkHighPtID_SF','F', lenVar='nMuon')
    self.out.branch('Muon_CutBased_TrkHighPtID_SFerr','F', lenVar='nMuon')

    self.out.branch('Muon_LooseRelIso_LooseID_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_LooseID_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_MediumID_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_MediumID_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_MediumPromptID_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_MediumPromptID_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_TightIDandIPCut_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelIso_TightIDandIPCut_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelTkIso_HighPtIDandIPCut_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelTkIso_HighPtIDandIPCut_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelIso_MediumID_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelIso_MediumID_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelIso_MediumPromptID_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelIso_MediumPromptID_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelIso_TightIDandIPCut_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelIso_TightIDandIPCut_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelTkIso_HighPtIDandIPCut_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelTkIso_HighPtIDandIPCut_SFerr', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelTkIso_TrkHighPtIDandIPCut_SF', 'F', lenVar='nMuon')
    self.out.branch('Muon_TightRelTkIso_TrkHighPtIDandIPCut_SFerr', 'F', lenVar='nMuon')

  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def analyze(self, event):
    
    muons = Collection(event, "Muon")
    if not (len(muons)>0): pass
    Muon_CutBased_LooseID_SF = []
    Muon_CutBased_LooseID_SFerr = []
    Muon_CutBased_MediumID_SF = []
    Muon_CutBased_MediumID_SFerr = []
    Muon_CutBased_MediumPromptID_SF = []
    Muon_CutBased_MediumPromptID_SFerr = []
    Muon_CutBased_TightID_SF = []
    Muon_CutBased_TightID_SFerr = []
    Muon_CutBased_SoftID_SF = []
    Muon_CutBased_SoftID_SFerr = []
    Muon_CutBased_HighPtID_SF = []
    Muon_CutBased_HighPtID_SFerr = []
    Muon_CutBased_TrkHighPtID_SF = []
    Muon_CutBased_TrkHighPtID_SFerr = []

    Muon_LooseRelIso_LooseID_SF = []
    Muon_LooseRelIso_MediumID_SF = []
    Muon_LooseRelIso_MediumPromptID_SF = []
    Muon_LooseRelIso_TightIDandIPCut_SF = []
    Muon_LooseRelTkIso_HighPtIDandIPCut_SF = []
    Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SF = []
    Muon_TightRelIso_MediumID_SF = []
    Muon_TightRelIso_MediumPromptID_SF = []
    Muon_TightRelIso_TightIDandIPCut_SF = []
    Muon_TightRelTkIso_HighPtIDandIPCut_SF = []
    Muon_TightRelTkIso_TrkHighPtIDandIPCut_SF = []
    Muon_LooseRelIso_LooseID_SFerr = []
    Muon_LooseRelIso_MediumID_SFerr = []
    Muon_LooseRelIso_MediumPromptID_SFerr = []
    Muon_LooseRelIso_TightIDandIPCut_SFerr = []
    Muon_LooseRelTkIso_HighPtIDandIPCut_SFerr = []
    Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SFerr = []
    Muon_TightRelIso_MediumID_SFerr = []
    Muon_TightRelIso_MediumPromptID_SFerr = []
    Muon_TightRelIso_TightIDandIPCut_SFerr = []
    Muon_TightRelTkIso_HighPtIDandIPCut_SFerr = []
    Muon_TightRelTkIso_TrkHighPtIDandIPCut_SFerr = []
    
    if len(muons)>0:
      for imu in range(0, len(muons)):
        if muons[imu].pt < 120: 
          Muon_CutBased_LooseID_SF.append(self.id_loose_th2f.GetBinContent(self.id_loose_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_LooseID_SFerr.append(self.id_loose_th2f.GetBinError(self.id_loose_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_MediumID_SF.append(self.id_medium_th2f.GetBinContent(self.id_medium_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_MediumID_SFerr.append(self.id_medium_th2f.GetBinError(self.id_medium_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_MediumPromptID_SF.append(self.id_mediumprompt_th2f.GetBinContent(self.id_mediumprompt_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_MediumPromptID_SFerr.append(self.id_mediumprompt_th2f.GetBinError(self.id_mediumprompt_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_TightID_SF.append(self.id_tight_th2f.GetBinContent(self.id_tight_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_TightID_SFerr.append(self.id_tight_th2f.GetBinError(self.id_tight_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_SoftID_SF.append(self.id_soft_th2f.GetBinContent(self.id_soft_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_SoftID_SFerr.append(self.id_soft_th2f.GetBinError(self.id_soft_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_HighPtID_SF.append(self.id_highpt_th2f.GetBinContent(self.id_highpt_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_HighPtID_SFerr.append(self.id_highpt_th2f.GetBinError(self.id_highpt_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_TrkHighPtID_SF.append(self.id_trkhighpt_th2f.GetBinContent(self.id_trkhighpt_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_CutBased_TrkHighPtID_SFerr.append(self.id_trkhighpt_th2f.GetBinError(self.id_trkhighpt_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))

          Muon_LooseRelIso_LooseID_SF.append(self.iso_looseRelIso_looseID_th2f.GetBinContent(self.iso_looseRelIso_looseID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_LooseID_SFerr.append(self.iso_looseRelIso_looseID_th2f.GetBinError(self.iso_looseRelIso_looseID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_MediumID_SF.append(self.iso_looseRelIso_mediumID_th2f.GetBinContent(self.iso_looseRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_MediumID_SFerr.append(self.iso_looseRelIso_mediumID_th2f.GetBinError(self.iso_looseRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_MediumPromptID_SF.append(self.iso_looseRelIso_mediumpromptID_th2f.GetBinContent(self.iso_looseRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_MediumPromptID_SFerr.append(self.iso_looseRelIso_mediumpromptID_th2f.GetBinError(self.iso_looseRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_TightIDandIPCut_SF.append(self.iso_looseRelIso_tightIDandIPCut_th2f.GetBinContent(self.iso_looseRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelIso_TightIDandIPCut_SFerr.append(self.iso_looseRelIso_tightIDandIPCut_th2f.GetBinError(self.iso_looseRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelTkIso_HighPtIDandIPCut_SF.append(self.iso_looseRelTkIso_highptIDandIPCut_th2f.GetBinContent(self.iso_looseRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelTkIso_HighPtIDandIPCut_SFerr.append(self.iso_looseRelTkIso_highptIDandIPCut_th2f.GetBinError(self.iso_looseRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SF.append(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.GetBinContent(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SFerr.append(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.GetBinError(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelIso_MediumID_SF.append(self.iso_tightRelIso_mediumID_th2f.GetBinContent(self.iso_tightRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelIso_MediumID_SFerr.append(self.iso_tightRelIso_mediumID_th2f.GetBinError(self.iso_tightRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelIso_MediumPromptID_SF.append(self.iso_tightRelIso_mediumpromptID_th2f.GetBinContent(self.iso_tightRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelIso_MediumPromptID_SFerr.append(self.iso_tightRelIso_mediumpromptID_th2f.GetBinError(self.iso_tightRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelIso_TightIDandIPCut_SF.append(self.iso_tightRelIso_tightIDandIPCut_th2f.GetBinContent(self.iso_tightRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelIso_TightIDandIPCut_SFerr.append(self.iso_tightRelIso_tightIDandIPCut_th2f.GetBinError(self.iso_tightRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelTkIso_HighPtIDandIPCut_SF.append(self.iso_tightRelTkIso_highptIDandIPCut_th2f.GetBinContent(self.iso_tightRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelTkIso_HighPtIDandIPCut_SFerr.append(self.iso_tightRelTkIso_highptIDandIPCut_th2f.GetBinError(self.iso_tightRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelTkIso_TrkHighPtIDandIPCut_SF.append(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.GetBinContent(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
          Muon_TightRelTkIso_TrkHighPtIDandIPCut_SFerr.append(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.GetBinError(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), muons[imu].pt)))
        else: 
          Muon_CutBased_LooseID_SF.append(self.id_loose_th2f.GetBinContent(self.id_loose_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_LooseID_SFerr.append(self.id_loose_th2f.GetBinError(self.id_loose_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_MediumID_SF.append(self.id_medium_th2f.GetBinContent(self.id_medium_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_MediumID_SFerr.append(self.id_medium_th2f.GetBinError(self.id_medium_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_MediumPromptID_SF.append(self.id_mediumprompt_th2f.GetBinContent(self.id_mediumprompt_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_MediumPromptID_SFerr.append(self.id_mediumprompt_th2f.GetBinError(self.id_mediumprompt_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_TightID_SF.append(self.id_tight_th2f.GetBinContent(self.id_tight_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_TightID_SFerr.append(self.id_tight_th2f.GetBinError(self.id_tight_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_SoftID_SF.append(self.id_soft_th2f.GetBinContent(self.id_soft_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_SoftID_SFerr.append(self.id_soft_th2f.GetBinError(self.id_soft_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_HighPtID_SF.append(self.id_highpt_th2f.GetBinContent(self.id_highpt_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_HighPtID_SFerr.append(self.id_highpt_th2f.GetBinError(self.id_highpt_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_TrkHighPtID_SF.append(self.id_trkhighpt_th2f.GetBinContent(self.id_trkhighpt_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_CutBased_TrkHighPtID_SFerr.append(self.id_trkhighpt_th2f.GetBinError(self.id_trkhighpt_th2f.FindBin(abs(muons[imu].eta), 119)))

          Muon_LooseRelIso_LooseID_SF.append(self.iso_looseRelIso_looseID_th2f.GetBinContent(self.iso_looseRelIso_looseID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_LooseID_SFerr.append(self.iso_looseRelIso_looseID_th2f.GetBinError(self.iso_looseRelIso_looseID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_MediumID_SF.append(self.iso_looseRelIso_mediumID_th2f.GetBinContent(self.iso_looseRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_MediumID_SFerr.append(self.iso_looseRelIso_mediumID_th2f.GetBinError(self.iso_looseRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_MediumPromptID_SF.append(self.iso_looseRelIso_mediumpromptID_th2f.GetBinContent(self.iso_looseRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_MediumPromptID_SFerr.append(self.iso_looseRelIso_mediumpromptID_th2f.GetBinError(self.iso_looseRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_TightIDandIPCut_SF.append(self.iso_looseRelIso_tightIDandIPCut_th2f.GetBinContent(self.iso_looseRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelIso_TightIDandIPCut_SFerr.append(self.iso_looseRelIso_tightIDandIPCut_th2f.GetBinError(self.iso_looseRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelTkIso_HighPtIDandIPCut_SF.append(self.iso_looseRelTkIso_highptIDandIPCut_th2f.GetBinContent(self.iso_looseRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelTkIso_HighPtIDandIPCut_SFerr.append(self.iso_looseRelTkIso_highptIDandIPCut_th2f.GetBinError(self.iso_looseRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SF.append(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.GetBinContent(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SFerr.append(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.GetBinError(self.iso_looseRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelIso_MediumID_SF.append(self.iso_tightRelIso_mediumID_th2f.GetBinContent(self.iso_tightRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelIso_MediumID_SFerr.append(self.iso_tightRelIso_mediumID_th2f.GetBinError(self.iso_tightRelIso_mediumID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelIso_MediumPromptID_SF.append(self.iso_tightRelIso_mediumpromptID_th2f.GetBinContent(self.iso_tightRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelIso_MediumPromptID_SFerr.append(self.iso_tightRelIso_mediumpromptID_th2f.GetBinError(self.iso_tightRelIso_mediumpromptID_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelIso_TightIDandIPCut_SF.append(self.iso_tightRelIso_tightIDandIPCut_th2f.GetBinContent(self.iso_tightRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelIso_TightIDandIPCut_SFerr.append(self.iso_tightRelIso_tightIDandIPCut_th2f.GetBinError(self.iso_tightRelIso_tightIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelTkIso_HighPtIDandIPCut_SF.append(self.iso_tightRelTkIso_highptIDandIPCut_th2f.GetBinContent(self.iso_tightRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelTkIso_HighPtIDandIPCut_SFerr.append(self.iso_tightRelTkIso_highptIDandIPCut_th2f.GetBinError(self.iso_tightRelTkIso_highptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelTkIso_TrkHighPtIDandIPCut_SF.append(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.GetBinContent(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))
          Muon_TightRelTkIso_TrkHighPtIDandIPCut_SFerr.append(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.GetBinError(self.iso_tightRelTkIso_trkhighptIDandIPCut_th2f.FindBin(abs(muons[imu].eta), 119)))


      self.out.fillBranch('Muon_CutBased_LooseID_SF', Muon_CutBased_LooseID_SF)
      self.out.fillBranch('Muon_CutBased_LooseID_SFerr', Muon_CutBased_LooseID_SFerr)
      self.out.fillBranch('Muon_CutBased_MediumID_SF', Muon_CutBased_MediumID_SF)
      self.out.fillBranch('Muon_CutBased_MediumID_SFerr', Muon_CutBased_MediumID_SFerr)
      self.out.fillBranch('Muon_CutBased_MediumPromptID_SF', Muon_CutBased_MediumPromptID_SF)
      self.out.fillBranch('Muon_CutBased_MediumPromptID_SFerr', Muon_CutBased_MediumPromptID_SFerr)
      self.out.fillBranch('Muon_CutBased_TightID_SF', Muon_CutBased_TightID_SF)
      self.out.fillBranch('Muon_CutBased_TightID_SFerr', Muon_CutBased_TightID_SFerr)
      self.out.fillBranch('Muon_CutBased_SoftID_SF', Muon_CutBased_SoftID_SF)
      self.out.fillBranch('Muon_CutBased_SoftID_SFerr', Muon_CutBased_SoftID_SFerr)
      self.out.fillBranch('Muon_CutBased_HighPtID_SF', Muon_CutBased_HighPtID_SF)
      self.out.fillBranch('Muon_CutBased_HighPtID_SFerr', Muon_CutBased_HighPtID_SFerr)
      self.out.fillBranch('Muon_CutBased_TrkHighPtID_SF', Muon_CutBased_TrkHighPtID_SF)
      self.out.fillBranch('Muon_CutBased_TrkHighPtID_SFerr', Muon_CutBased_TrkHighPtID_SFerr)

      self.out.fillBranch('Muon_LooseRelIso_LooseID_SF', Muon_LooseRelIso_LooseID_SF)
      self.out.fillBranch('Muon_LooseRelIso_LooseID_SFerr', Muon_LooseRelIso_LooseID_SFerr)
      self.out.fillBranch('Muon_LooseRelIso_MediumID_SF', Muon_LooseRelIso_MediumID_SF)
      self.out.fillBranch('Muon_LooseRelIso_MediumID_SFerr', Muon_LooseRelIso_MediumID_SFerr)
      self.out.fillBranch('Muon_LooseRelIso_MediumPromptID_SF', Muon_LooseRelIso_MediumPromptID_SF)
      self.out.fillBranch('Muon_LooseRelIso_MediumPromptID_SFerr', Muon_LooseRelIso_MediumPromptID_SFerr)
      self.out.fillBranch('Muon_LooseRelIso_TightIDandIPCut_SF', Muon_LooseRelIso_TightIDandIPCut_SF)
      self.out.fillBranch('Muon_LooseRelIso_TightIDandIPCut_SFerr', Muon_LooseRelIso_TightIDandIPCut_SFerr)
      self.out.fillBranch('Muon_LooseRelTkIso_HighPtIDandIPCut_SF', Muon_LooseRelTkIso_HighPtIDandIPCut_SF)
      self.out.fillBranch('Muon_LooseRelTkIso_HighPtIDandIPCut_SFerr', Muon_LooseRelTkIso_HighPtIDandIPCut_SFerr)
      self.out.fillBranch('Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SF', Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SF)
      self.out.fillBranch('Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SFerr', Muon_LooseRelTkIso_TrkHighPtIDandIPCut_SFerr)
      self.out.fillBranch('Muon_TightRelIso_MediumID_SF', Muon_TightRelIso_MediumID_SF)
      self.out.fillBranch('Muon_TightRelIso_MediumID_SFerr', Muon_TightRelIso_MediumID_SFerr)
      self.out.fillBranch('Muon_TightRelIso_MediumPromptID_SF',Muon_TightRelIso_MediumPromptID_SF)
      self.out.fillBranch('Muon_TightRelIso_MediumPromptID_SFerr',Muon_TightRelIso_MediumPromptID_SFerr)
      self.out.fillBranch('Muon_TightRelIso_TightIDandIPCut_SF',Muon_TightRelIso_TightIDandIPCut_SF)
      self.out.fillBranch('Muon_TightRelIso_TightIDandIPCut_SFerr',Muon_TightRelIso_TightIDandIPCut_SFerr)
      self.out.fillBranch('Muon_TightRelTkIso_HighPtIDandIPCut_SF',Muon_TightRelTkIso_HighPtIDandIPCut_SF)
      self.out.fillBranch('Muon_TightRelTkIso_HighPtIDandIPCut_SFerr',Muon_TightRelTkIso_HighPtIDandIPCut_SFerr)
      self.out.fillBranch('Muon_TightRelTkIso_TrkHighPtIDandIPCut_SF',Muon_TightRelTkIso_TrkHighPtIDandIPCut_SF)
      self.out.fillBranch('Muon_TightRelTkIso_TrkHighPtIDandIPCut_SFerr',Muon_TightRelTkIso_TrkHighPtIDandIPCut_SFerr)

    return True

muonIDISOSF2016 = lambda: muonIDISOSFProducer("2016")
muonIDISOSF2017 = lambda: muonIDISOSFProducer("2017")
muonIDISOSF2018 = lambda: muonIDISOSFProducer("2018")
