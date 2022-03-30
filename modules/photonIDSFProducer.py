# SF given by https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
# !!! Correction Lib is not supported currently !!!
# This method is refer to: https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaSFJSON
# First you need to install the correctionlib library
# python3 -m pip install git+https://github.com/cms-nanoAOD/correctionlib.git
# The json files are given by: https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/EGM
# Or you can also find them in: /cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import math
import os

class phoIDSFProducer(Module):
    def __init__( self , year ):
        self.year = year
        self.year_tag_map = {"2016Pre":"UL16", "2016Post":"UL16_postVFP", "2017":"UL17", "2018":"UL18"}
        self.id_loose = "egammaEffi.txt_EGM2D_Pho_Loose_%s.root" %(self.year_tag_map[self.year])
        self.id_medium = "egammaEffi.txt_EGM2D_Pho_Medium_%s.root" %(self.year_tag_map[self.year])
        self.id_tight = "egammaEffi.txt_EGM2D_Pho_Tight_%s.root" %(self.year_tag_map[self.year])
        self.SF_location_path = "%s/src/PhysicsTools/NanoAODTools/data/EG_photon/%s/" %(os.environ['CMSSW_BASE'], self.year)
        print 'SF location:', self.SF_location_path

    def beginJob(self):
        print 'begin to set Photon ID SF --->>>'
        print 'start to open SF root file --->>>'
        # init the TH2F
        self.id_loose_th2f = ROOT.TH2F()
        self.id_medium_th2f = ROOT.TH2F()
        self.id_tight_th2f = ROOT.TH2F()
        #Open the SF root file
        self.file_id_loose = ROOT.TFile.Open(self.SF_location_path+self.id_loose)
        self.file_id_medium = ROOT.TFile.Open(self.SF_location_path+self.id_medium)
        self.file_id_tight = ROOT.TFile.Open(self.SF_location_path+self.id_tight)
        #access to the TH2F
        self.file_id_loose.GetObject('EGamma_SF2D', self.id_loose_th2f)
        self.file_id_medium.GetObject('EGamma_SF2D', self.id_medium_th2f)
        self.file_id_tight.GetObject('EGamma_SF2D', self.id_tight_th2f)
        print 'open SF files successfully --->>>'

    def endJob(self):
        print 'close SF root file --->>>'
        self.file_id_loose.Close()
        self.file_id_medium.Close()
        self.file_id_tight.Close()
        print 'finish setting Photon ID SF --->>>'
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('Photon_CutBased_LooseID_SF','F', lenVar='nPhoton')
        self.out.branch('Photon_CutBased_LooseID_SFerr','F', lenVar='nPhoton')
        self.out.branch('Photon_CutBased_MediumID_SF','F', lenVar='nPhoton')
        self.out.branch('Photon_CutBased_MediumID_SFerr','F', lenVar='nPhoton')
        self.out.branch('Photon_CutBased_TightID_SF','F', lenVar='nPhoton')
        self.out.branch('Photon_CutBased_TightID_SFerr','F', lenVar='nPhoton')
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        
        photons = Collection(event, "Photon")
        if not (len(photons)>0): pass
        Photon_CutBased_LooseID_SF = []
        Photon_CutBased_LooseID_SFerr = []
        Photon_CutBased_MediumID_SF = []
        Photon_CutBased_MediumID_SFerr = []
        Photon_CutBased_TightID_SF = []
        Photon_CutBased_TightID_SFerr = []
        
        for iele in range(0, len(photons)):
            if photons[iele].pt < 500: 
                Photon_CutBased_LooseID_SF.append(self.id_loose_th2f.GetBinContent(self.id_loose_th2f.FindBin(photons[iele].eta, photons[iele].pt)))
                Photon_CutBased_LooseID_SFerr.append(self.id_loose_th2f.GetBinError(self.id_loose_th2f.FindBin(photons[iele].eta, photons[iele].pt)))
                Photon_CutBased_MediumID_SF.append(self.id_medium_th2f.GetBinContent(self.id_medium_th2f.FindBin(photons[iele].eta, photons[iele].pt)))
                Photon_CutBased_MediumID_SFerr.append(self.id_medium_th2f.GetBinError(self.id_medium_th2f.FindBin(photons[iele].eta, photons[iele].pt)))
                Photon_CutBased_TightID_SF.append(self.id_tight_th2f.GetBinContent(self.id_tight_th2f.FindBin(photons[iele].eta, photons[iele].pt)))
                Photon_CutBased_TightID_SFerr.append(self.id_tight_th2f.GetBinError(self.id_tight_th2f.FindBin(photons[iele].eta, photons[iele].pt)))
            else: 
                Photon_CutBased_LooseID_SF.append(self.id_loose_th2f.GetBinContent(self.id_loose_th2f.FindBin(photons[iele].eta, 499)))
                Photon_CutBased_LooseID_SFerr.append(self.id_loose_th2f.GetBinError(self.id_loose_th2f.FindBin(photons[iele].eta, 499)))
                Photon_CutBased_MediumID_SF.append(self.id_medium_th2f.GetBinContent(self.id_medium_th2f.FindBin(photons[iele].eta, 499)))
                Photon_CutBased_MediumID_SFerr.append(self.id_medium_th2f.GetBinError(self.id_medium_th2f.FindBin(photons[iele].eta, 499)))
                Photon_CutBased_TightID_SF.append(self.id_tight_th2f.GetBinContent(self.id_tight_th2f.FindBin(photons[iele].eta, 499)))
                Photon_CutBased_TightID_SFerr.append(self.id_tight_th2f.GetBinError(self.id_tight_th2f.FindBin(photons[iele].eta, 499)))
        self.out.fillBranch('Photon_CutBased_LooseID_SF', Photon_CutBased_LooseID_SF)
        self.out.fillBranch('Photon_CutBased_LooseID_SFerr', Photon_CutBased_LooseID_SFerr)
        self.out.fillBranch('Photon_CutBased_MediumID_SF', Photon_CutBased_MediumID_SF)
        self.out.fillBranch('Photon_CutBased_MediumID_SFerr', Photon_CutBased_MediumID_SFerr)
        self.out.fillBranch('Photon_CutBased_TightID_SF', Photon_CutBased_TightID_SF)
        self.out.fillBranch('Photon_CutBased_TightID_SFerr', Photon_CutBased_TightID_SFerr)

        return True

phoIDSF2016Pre = lambda: phoIDSFProducer("2016Pre")
phoIDSF2016Post = lambda: phoIDSFProducer("2016Post")
phoIDSF2017 = lambda: phoIDSFProducer("2017")
phoIDSF2018 = lambda: phoIDSFProducer("2018")
