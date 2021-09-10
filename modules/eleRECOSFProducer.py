import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import math
import os

class eleRECOSFProducer(Module):
  def __init__( self , year ):
    self.year = year
    self.reco_input1 = "egamma_RECO_low.root"
    self.reco_input2 = "egamma_RECO_high.root"
    self.SF_location_path = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/data/year%s/" %(os.environ['CMSSW_BASE'], self.year)
#    print 'SF location:', self.SF_location_path

  def beginJob(self):
    print 'begin to set Electron and Photon RECO SF --->>>'
    print 'start to open SF root file --->>>'
    self.reco_th2f_low = ROOT.TH2F()
    self.reco_th2f_high = ROOT.TH2F()
    self.file_reco_th2f_low = ROOT.TFile.Open(self.SF_location_path+self.reco_input1)
    self.file_reco_th2f_high = ROOT.TFile.Open(self.SF_location_path+self.reco_input2)
    self.file_reco_th2f_low.GetObject('EGamma_SF2D', self.reco_th2f_low)
    self.file_reco_th2f_high.GetObject('EGamma_SF2D', self.reco_th2f_high)
    print 'open SF files successfully --->>>'

  def endJob(self):
    print 'close SF root file --->>>'
    self.file_reco_th2f_low.Close()
    self.file_reco_th2f_high.Close()
    print 'finish setting Electron and Photon RECO and SF --->>>'
    
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch('Electron_RECO_SF','F', lenVar='nElectron')
    self.out.branch('Electron_RECO_SFerr','F', lenVar='nElectron')
  def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    pass

  def analyze(self, event):
    
    electrons = Collection(event, "Electron")
    if not (len(electrons)>0): pass
    Electron_RECO_SF = []
    Electron_RECO_SFerr = []
    
    for iele in range(0, len(electrons)):
      if electrons[iele].pt < 20: 
        Electron_RECO_SF.append(self.reco_th2f_low.GetBinContent(self.reco_th2f_low.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_RECO_SFerr.append(self.reco_th2f_low.GetBinError(self.reco_th2f_low.FindBin(electrons[iele].eta, electrons[iele].pt)))
      if electrons[iele].pt >= 20 and electrons[iele].pt < 500:
        Electron_RECO_SF.append(self.reco_th2f_high.GetBinContent(self.reco_th2f_high.FindBin(electrons[iele].eta, electrons[iele].pt)))
        Electron_RECO_SFerr.append(self.reco_th2f_high.GetBinError(self.reco_th2f_high.FindBin(electrons[iele].eta, electrons[iele].pt)))
      if electrons[iele].pt >= 500:
        Electron_RECO_SF.append(self.reco_th2f_high.GetBinContent(self.reco_th2f_high.FindBin(electrons[iele].eta, 499)))
        Electron_RECO_SFerr.append(self.reco_th2f_high.GetBinError(self.reco_th2f_high.FindBin(electrons[iele].eta, 499)))
    self.out.fillBranch('Electron_RECO_SF', Electron_RECO_SF)
    self.out.fillBranch('Electron_RECO_SFerr', Electron_RECO_SFerr)

    return True

eleRECOSF2016 = lambda: eleRECOSFProducer("2016")
eleRECOSF2017 = lambda: eleRECOSFProducer("2017")
eleRECOSF2018 = lambda: eleRECOSFProducer("2018")
