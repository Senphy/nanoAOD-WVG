import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import math
import os

class btagWeightProducer_1a(Module):
    def __init__(self):
        pass

    def Cal_temp_weight(self, pt, eta, hist):
        BinX = hist.GetXaxis().FindBin(pt)
        BinY = hist.GetXaxis().FindBin(eta)
        if BinX > hist.GetNbinsX():
            BinX = hist.GetNbinsX()
        if BinY > hist.GetNbinsY():
            BinY = hist.GetNbinsY()
        return hist.GetBinContent(BinX, BinY)
        pass

    def divi(self, a, b):
        try:
            return a / b
        except ZeroDivisionError as zde:
            return 1
        except Exception as e:
            raise e

    def beginJob(self):
        self.h_btag_bjet = ROOT.TH2D()
        self.h_btag_cjet = ROOT.TH2D()
        self.h_btag_ljet = ROOT.TH2D()
        self.h_bjet = ROOT.TH2D()
        self.h_cjet = ROOT.TH2D()
        self.h_ljet = ROOT.TH2D()
        pass

    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        inputFile.GetObject('h_btag_bjet', self.h_btag_bjet)
        inputFile.GetObject('h_btag_cjet', self.h_btag_cjet)
        inputFile.GetObject('h_btag_ljet', self.h_btag_ljet)
        inputFile.GetObject('h_bjet', self.h_bjet)
        inputFile.GetObject('h_cjet', self.h_cjet)
        inputFile.GetObject('h_ljet', self.h_ljet)
        self.out = wrappedOutputTree
        self.out.branch('btagWeight', 'F')
        self.out.branch('btagWeight_bc_up', 'F')
        self.out.branch('btagWeight_bc_down', 'F')
        self.out.branch('btagWeight_bc_up_corr', 'F')
        self.out.branch('btagWeight_bc_down_corr', 'F')
        self.out.branch('btagWeight_bc_up_uncorr', 'F')
        self.out.branch('btagWeight_bc_down_uncorr', 'F')
        self.out.branch('btagWeight_l_up', 'F')
        self.out.branch('btagWeight_l_down', 'F')
        self.out.branch('btagWeight_l_up_corr', 'F')
        self.out.branch('btagWeight_l_down_corr', 'F')
        self.out.branch('btagWeight_l_up_uncorr', 'F')
        self.out.branch('btagWeight_l_down_uncorr', 'F')
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        jets = Collection(event, "Jet")
        tight_jets = []
        tight_bjets = []
        for i in range(0, event.nJets):
            tight_jets.append(event.TightJets_index[i])
        for i in range(0, event.nbJets):
            tight_bjets.append(event.TightbJets_index[i])

        btagWeight = 1.
        btagWeight_bc_up = 1.
        btagWeight_bc_down = 1.
        btagWeight_bc_up_corr = 1.
        btagWeight_bc_down_corr = 1.
        btagWeight_bc_up_uncorr = 1.
        btagWeight_bc_down_uncorr = 1.
        btagWeight_l_up = 1.
        btagWeight_l_down = 1.
        btagWeight_l_up_corr = 1.
        btagWeight_l_down_corr = 1.
        btagWeight_l_up_uncorr = 1.
        btagWeight_l_down_uncorr = 1.
        pmc = 1.
        pdata = 1.
        pdata_bc_up = 1.
        pdata_bc_down = 1.
        pdata_bc_up_corr = 1.
        pdata_bc_down_corr = 1.
        pdata_bc_up_uncorr = 1.
        pdata_bc_down_uncorr = 1.
        pdata_l_up = 1.
        pdata_l_down = 1.
        pdata_l_up_corr = 1.
        pdata_l_down_corr = 1.
        pdata_l_up_uncorr = 1.
        pdata_l_down_uncorr = 1.
        for i in tight_jets:
            temp_weight = 1.
            # tagged
            if i in tight_bjets:
                if jets[i].hadronFlavour == 5 or jets[i].hadronFlavour == 4 :
                    if jets[i].hadronFlavour == 5:
                        temp_weight = self.divi(self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_btag_bjet), self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_bjet))
                    elif jets[i].hadronFlavour == 4:
                        temp_weight = self.divi(self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_btag_cjet), self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_cjet))
                    pdata_bc_up *= getattr(event, "Jet_btagSF_deepcsv_T_up")[i] * temp_weight
                    pdata_bc_down *= getattr(event, "Jet_btagSF_deepcsv_T_down")[i] * temp_weight
                    pdata_bc_up_corr *= getattr(event, "Jet_btagSF_deepcsv_T_up_correlated")[i] * temp_weight
                    pdata_bc_down_corr *= getattr(event, "Jet_btagSF_deepcsv_T_down_correlated")[i] * temp_weight
                    pdata_bc_up_uncorr *= getattr(event, "Jet_btagSF_deepcsv_T_up_uncorrelated")[i] * temp_weight
                    pdata_bc_down_uncorr *= getattr(event, "Jet_btagSF_deepcsv_T_down_uncorrelated")[i] * temp_weight

                elif jets[i].hadronFlavour == 0:
                    temp_weight = self.divi(self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_btag_ljet), self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_ljet))
                    pdata_l_up *= getattr(event, "Jet_btagSF_deepcsv_T_up")[i] * temp_weight
                    pdata_l_down *= getattr(event, "Jet_btagSF_deepcsv_T_down")[i] * temp_weight
                    pdata_l_up_corr *= getattr(event, "Jet_btagSF_deepcsv_T_up_correlated")[i] * temp_weight
                    pdata_l_down_corr *= getattr(event, "Jet_btagSF_deepcsv_T_down_correlated")[i] * temp_weight
                    pdata_l_up_uncorr *= getattr(event, "Jet_btagSF_deepcsv_T_up_uncorrelated")[i] * temp_weight
                    pdata_l_down_uncorr *= getattr(event, "Jet_btagSF_deepcsv_T_down_uncorrelated")[i] * temp_weight

                pmc *= temp_weight
                pdata *= getattr(event, "Jet_btagSF_deepcsv_T")[i] * temp_weight

            # not tagged
            else:
                if jets[i].hadronFlavour == 5 or jets[i].hadronFlavour == 4 :
                    if jets[i].hadronFlavour == 5:
                        temp_weight = self.divi(self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_btag_bjet), self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_bjet))
                    elif jets[i].hadronFlavour == 4:
                        temp_weight = self.divi(self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_btag_cjet), self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_cjet))
                    pdata_bc_up *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_up")[i] * temp_weight)
                    pdata_bc_down *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_down")[i] * temp_weight)
                    pdata_bc_up_corr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_up_correlated")[i] * temp_weight)
                    pdata_bc_down_corr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_down_correlated")[i] * temp_weight)
                    pdata_bc_up_uncorr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_up_uncorrelated")[i] * temp_weight)
                    pdata_bc_down_uncorr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_down_uncorrelated")[i] * temp_weight)

                elif jets[i].hadronFlavour == 0:
                    temp_weight = self.divi(self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_btag_ljet), self.Cal_temp_weight(jets[i].pt, jets[i].eta, self.h_ljet))
                    # notice the sign here
                    pdata_l_up *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_up")[i] * temp_weight)
                    pdata_l_down *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_down")[i] * temp_weight)
                    pdata_l_up_corr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_up_correlated")[i] * temp_weight)
                    pdata_l_down_corr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_down_correlated")[i] * temp_weight)
                    pdata_l_up_uncorr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_up_uncorrelated")[i] * temp_weight)
                    pdata_l_down_uncorr *= (1 - getattr(event, "Jet_btagSF_deepcsv_T_down_uncorrelated")[i] * temp_weight)
                pmc *= (1 - temp_weight)
                pdata *= (1 - getattr(event, "Jet_btagSF_deepcsv_T")[i] * temp_weight)

        if pmc != 0: 
            btagWeight = pdata/pmc
            btagWeight_bc_up = pdata_bc_up/pmc
            btagWeight_bc_down = pdata_bc_down/pmc
            btagWeight_bc_up_corr = pdata_bc_up_corr/pmc
            btagWeight_bc_down_corr = pdata_bc_down_corr/pmc
            btagWeight_bc_up_uncorr = pdata_bc_up_uncorr/pmc
            btagWeight_bc_down_uncorr = pdata_bc_down_uncorr/pmc
            btagWeight_l_up = pdata_l_up/pmc
            btagWeight_l_down = pdata_l_down/pmc
            btagWeight_l_up_corr = pdata_l_up_corr/pmc
            btagWeight_l_down_corr = pdata_l_down_corr/pmc
            btagWeight_l_up_uncorr = pdata_l_up_uncorr/pmc
            btagWeight_l_down_uncorr = pdata_l_down_uncorr/pmc

        self.out.fillBranch('btagWeight', btagWeight)
        self.out.fillBranch('btagWeight_bc_up', btagWeight_bc_up)
        self.out.fillBranch('btagWeight_bc_down', btagWeight_bc_down)
        self.out.fillBranch('btagWeight_bc_up_corr', btagWeight_bc_up_corr)
        self.out.fillBranch('btagWeight_bc_down_corr', btagWeight_bc_down_corr)
        self.out.fillBranch('btagWeight_bc_up_uncorr', btagWeight_bc_up_uncorr)
        self.out.fillBranch('btagWeight_bc_down_uncorr', btagWeight_bc_down_uncorr)
        self.out.fillBranch('btagWeight_l_up', btagWeight_l_up)
        self.out.fillBranch('btagWeight_l_down', btagWeight_l_down)
        self.out.fillBranch('btagWeight_l_up_corr', btagWeight_l_up_corr)
        self.out.fillBranch('btagWeight_l_down_corr', btagWeight_l_down_corr)
        self.out.fillBranch('btagWeight_l_up_uncorr', btagWeight_l_up_uncorr)
        self.out.fillBranch('btagWeight_l_down_uncorr', btagWeight_l_down_uncorr)

        return True

btagWeight_1a_Module = lambda: btagWeightProducer_1a()
