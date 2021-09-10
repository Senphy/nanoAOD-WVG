import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import math
import os

class eleIDSFProducer(Module):
  def __init__( self , year ):
    self.year = year
    self.id_veto = "ele_Veto.root"
    self.id_loose = "ele_Loose.root"
    self.id_medium = "ele_Medium.root"
    self.id_tight = "ele_Tight.root"
    self.id_mva80iso = "ele_MVA80iso.root"
    self.id_mva80noiso = "ele_MVA80noIso.root"
    self.id_mva90iso = "ele_MVA90iso.root"
    self.id_mva90noiso = "ele_MVA90noIso.root"
    self.SF_location_path = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/data/year%s/" %(os.environ['CMSSW_BASE'], self.year)
    print 'SF location:', self.SF_location_path

  def beginJob(self):
    print 'begin to set Electron ID SF --->>>'
    print 'start to open SF root file --->>>'
    # init the TH2F
    self.id_veto_th2f= ROOT.TH2F()
    self.id_loose_th2f= ROOT.TH2F()
    self.id_medium_th2f= ROOT.TH2F()
    self.id_tight_th2f= ROOT.TH2F()
    self.id_mva80iso_th2f= ROOT.TH2F()
    self.id_mva80noiso_th2f= ROOT.TH2F()
    self.id_mva90iso_th2f= ROOT.TH2F()
    self.id_mva90noiso_th2f= ROOT.TH2F()
    #Open the SF root file
    self.file_id_veto= ROOT.TFile.Open(self.SF_location_path+self.id_veto)
    self.file_id_loose= ROOT.TFile.Open(self.SF_location_path+self.id_loose)
    self.file_id_medium= ROOT.TFile.Open(self.SF_location_path+self.id_medium)
    self.file_id_tight= ROOT.TFile.Open(self.SF_location_path+self.id_tight)
    self.file_id_mva80iso= ROOT.TFile.Open(self.SF_location_path+self.id_mva80iso)
    self.file_id_mva80noiso= ROOT.TFile.Open(self.SF_location_path+self.id_mva80noiso)
    self.file_id_mva90iso= ROOT.TFile.Open(self.SF_location_path+self.id_mva90iso)
    self.file_id_mva90noiso= ROOT.TFile.Open(self.SF_location_path+self.id_mva90noiso)
    #access to the TH2F
    self.file_id_veto.GetObject('EGamma_SF2D', self.id_veto_th2f)
    self.file_id_loose.GetObject('EGamma_SF2D', self.id_loose_th2f)
    self.file_id_medium.GetObject('EGamma_SF2D', self.id_medium_th2f)
    self.file_id_tight.GetObject('EGamma_SF2D', self.id_tight_th2f)
    self.file_id_mva80iso.GetObject('EGamma_SF2D', self.id_mva80iso_th2f)
    self.file_id_mva80noiso.GetObject('EGamma_SF2D', self.id_mva80noiso_th2f)
    self.file_id_mva90iso.GetObject('EGamma_SF2D', self.id_mva90iso_th2f)
    self.file_id_mva90noiso.GetObject('EGamma_SF2D', self.id_mva90noiso_th2f)
    print 'open SF files successfully --->>>'

  def endJob(self):
    print 'close SF root file --->>>'
    self.file_id_veto.Close()
    self.file_id_loose.Close()
    self.file_id_medium.Close()
    self.file_id_tight.Close()
    self.file_id_mva80iso.Close()
    self.file_id_mva80noiso.Close()
    self.file_id_mva90iso.Close()
    self.file_id_mva90noiso.Close()
    print 'finish setting Electron ID SF --->>>'
    
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch('Electron_CutBased_VetoID_SF','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_VetoID_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_LooseID_SF','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_LooseID_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_MediumID_SF','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_MediumID_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_TightID_SF','F', lenVar='nElectron')
    self.out.branch('Electron_CutBased_TightID_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2Iso_WP80_SF','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2Iso_WP80_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2Iso_WP90_SF','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2Iso_WP90_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2noIso_WP80_SF','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2noIso_WP80_SFerr','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2noIso_WP90_SF','F', lenVar='nElectron')
    self.out.branch('Electron_MVAFall17V2noIso_WP90_SFerr','F', lenVar='nElectron')
  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def analyze(self, event):
    
    electrons = Collection(event, "Electron")
    if not (len(electrons)>0): pass
    Electron_CutBased_VetoID_SF = []
    Electron_CutBased_VetoID_SFerr = []
    Electron_CutBased_LooseID_SF = []
    Electron_CutBased_LooseID_SFerr = []
    Electron_CutBased_MediumID_SF = []
    Electron_CutBased_MediumID_SFerr = []
    Electron_CutBased_TightID_SF = []
    Electron_CutBased_TightID_SFerr = []
    Electron_MVAFall17V2Iso_WP80_SF = []
    Electron_MVAFall17V2Iso_WP80_SFerr = []
    Electron_MVAFall17V2Iso_WP90_SF = []
    Electron_MVAFall17V2Iso_WP90_SFerr = []
    Electron_MVAFall17V2noIso_WP80_SF = []
    Electron_MVAFall17V2noIso_WP80_SFerr = []
    Electron_MVAFall17V2noIso_WP90_SF = []
    Electron_MVAFall17V2noIso_WP90_SFerr = []
    
    for iele in range(0, len(electrons)):
      if electrons[iele].pt < 500: 
        Electron_CutBased_VetoID_SF.append(self.id_veto_th2f.GetBinContent(self.id_veto_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_VetoID_SFerr.append(self.id_veto_th2f.GetBinError(self.id_veto_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_LooseID_SF.append(self.id_loose_th2f.GetBinContent(self.id_loose_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_LooseID_SFerr.append(self.id_loose_th2f.GetBinError(self.id_loose_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_MediumID_SF.append(self.id_medium_th2f.GetBinContent(self.id_medium_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_MediumID_SFerr.append(self.id_medium_th2f.GetBinError(self.id_medium_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_TightID_SF.append(self.id_tight_th2f.GetBinContent(self.id_tight_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_CutBased_TightID_SFerr.append(self.id_tight_th2f.GetBinError(self.id_tight_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2Iso_WP80_SF.append(self.id_mva80iso_th2f.GetBinContent(self.id_mva80iso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2Iso_WP80_SFerr.append(self.id_mva80iso_th2f.GetBinError(self.id_mva80iso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2Iso_WP90_SF.append(self.id_mva90iso_th2f.GetBinContent(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2Iso_WP90_SFerr.append(self.id_mva90iso_th2f.GetBinError(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2noIso_WP80_SF.append(self.id_mva80noiso_th2f.GetBinContent(self.id_mva80noiso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2noIso_WP80_SFerr.append(self.id_mva80noiso_th2f.GetBinError(self.id_mva80noiso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2noIso_WP90_SF.append(self.id_mva90iso_th2f.GetBinContent(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_MVAFall17V2noIso_WP90_SFerr.append(self.id_mva90iso_th2f.GetBinError(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, electrons[iele].pt)))
      else: 
        Electron_CutBased_VetoID_SF.append(self.id_veto_th2f.GetBinContent(self.id_veto_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_VetoID_SFerr.append(self.id_veto_th2f.GetBinError(self.id_veto_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_LooseID_SF.append(self.id_loose_th2f.GetBinContent(self.id_loose_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_LooseID_SFerr.append(self.id_loose_th2f.GetBinError(self.id_loose_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_MediumID_SF.append(self.id_medium_th2f.GetBinContent(self.id_medium_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_MediumID_SFerr.append(self.id_medium_th2f.GetBinError(self.id_medium_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_TightID_SF.append(self.id_tight_th2f.GetBinContent(self.id_tight_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_CutBased_TightID_SFerr.append(self.id_tight_th2f.GetBinError(self.id_tight_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2Iso_WP80_SF.append(self.id_mva80iso_th2f.GetBinContent(self.id_mva80iso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2Iso_WP80_SFerr.append(self.id_mva80iso_th2f.GetBinError(self.id_mva80iso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2Iso_WP90_SF.append(self.id_mva90iso_th2f.GetBinContent(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2Iso_WP90_SFerr.append(self.id_mva90iso_th2f.GetBinError(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2noIso_WP80_SF.append(self.id_mva80noiso_th2f.GetBinContent(self.id_mva80noiso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2noIso_WP80_SFerr.append(self.id_mva80noiso_th2f.GetBinError(self.id_mva80noiso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2noIso_WP90_SF.append(self.id_mva90iso_th2f.GetBinContent(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, 499)))
        Electron_MVAFall17V2noIso_WP90_SFerr.append(self.id_mva90iso_th2f.GetBinError(self.id_mva90iso_th2f.FindBin(electrons[iele].eta, 499)))
    self.out.fillBranch('Electron_CutBased_VetoID_SF', Electron_CutBased_VetoID_SF)
    self.out.fillBranch('Electron_CutBased_VetoID_SFerr', Electron_CutBased_VetoID_SFerr)
    self.out.fillBranch('Electron_CutBased_LooseID_SF', Electron_CutBased_LooseID_SF)
    self.out.fillBranch('Electron_CutBased_LooseID_SFerr', Electron_CutBased_LooseID_SFerr)
    self.out.fillBranch('Electron_CutBased_MediumID_SF', Electron_CutBased_MediumID_SF)
    self.out.fillBranch('Electron_CutBased_MediumID_SFerr', Electron_CutBased_MediumID_SFerr)
    self.out.fillBranch('Electron_CutBased_TightID_SF', Electron_CutBased_TightID_SF)
    self.out.fillBranch('Electron_CutBased_TightID_SFerr', Electron_CutBased_TightID_SFerr)
    self.out.fillBranch('Electron_MVAFall17V2Iso_WP80_SF', Electron_MVAFall17V2Iso_WP80_SF)
    self.out.fillBranch('Electron_MVAFall17V2Iso_WP80_SFerr', Electron_MVAFall17V2Iso_WP80_SFerr)
    self.out.fillBranch('Electron_MVAFall17V2Iso_WP90_SF', Electron_MVAFall17V2Iso_WP90_SF)
    self.out.fillBranch('Electron_MVAFall17V2Iso_WP90_SFerr', Electron_MVAFall17V2Iso_WP90_SFerr)
    self.out.fillBranch('Electron_MVAFall17V2noIso_WP80_SF', Electron_MVAFall17V2noIso_WP80_SF)
    self.out.fillBranch('Electron_MVAFall17V2noIso_WP80_SFerr', Electron_MVAFall17V2noIso_WP80_SFerr)
    self.out.fillBranch('Electron_MVAFall17V2noIso_WP90_SF', Electron_MVAFall17V2noIso_WP90_SF)
    self.out.fillBranch('Electron_MVAFall17V2noIso_WP90_SFerr', Electron_MVAFall17V2noIso_WP90_SFerr)

    return True

eleIDSF2016 = lambda: eleIDSFProducer("2016")
eleIDSF2017 = lambda: eleIDSFProducer("2017")
eleIDSF2018 = lambda: eleIDSFProducer("2018")
