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



class ApplyWeightFakePhotonProducer(Module):
    def __init__(self, year):
        pass
        self.year = year
        self.unc_list = ['stat', 'iso', 'closure', 'mc']
        # stat: absolute value
        # other sys: relative value
        self.endcap_pt_map = {
            "2016":{
                "ptbins":[15, 50, 5000],
                "weight":[0.204, 0.111],
                "unc":{
                    "stat":[0.005, 0.013],
                    "iso":[0.089, 0.024],
                    "closure":[0.112, 0.130],
                    "mc":[0.017, 0.034],
                }
            },
            "2017":{
                "ptbins":[15, 50, 5000],
                "weight":[0.184, 0.074],
                "unc":{
                    "stat":[0.005, 0.011],
                    "iso":[0.023, 0.195],
                    "closure":[0.466, 0.476],
                    "mc":[0.065, 0.054],
                }
            },
            "2018":{
                "ptbins":[15, 50, 5000],
                "weight":[0.178, 0.099],
                "unc":{
                    "stat":[0.004, 0.010],
                    "iso":[0.003, 0.126],
                    "closure":[0.364, 0.406],
                    "mc":[0.049, 0.125],
                }
            }
        }

        self.barrel_pt_map = {
            "2016":{
                "ptbins":[15, 20, 30, 50, 70, 100, 5000],
                "weight":[0.285, 0.224, 0.159, 0.111, 0.109, 0.066],
                "unc":{
                    "stat":[0.005, 0.005, 0.006, 0.008, 0.010, 0.008],
                    "iso":[0.004, 0.025, 0.038, 0.001, 0.148, 0.045],
                    "closure":[0.157, 0.081, 0.008, 0.034, 0.061, 0.104],
                    "mc":[0.049, 0.017, 0.037, 0.242, 0.104, 0.108],
                }
            },
            "2017":{
                "ptbins":[15, 20, 30, 50, 70, 100, 5000],
                "weight":[0.278, 0.234, 0.159, 0.114, 0.075, 0.054],
                "unc":{
                    "stat":[0.004, 0.004, 0.005, 0.006, 0.006, 0.006],
                    "iso":[0.015, 0.002, 0.052, 0.083, 0.001, 0.050],
                    "closure":[0.168, 0.231, 0.035, 0.105, 0.690, 0.083],
                    "mc":[0.029, 0.038, 0.179, 0.081, 0.066, 0.138],
                }
            },
            "2018":{
                "ptbins":[15, 20, 30, 50, 70, 100, 5000],
                "weight":[0.261, 0.227, 0.159, 0.113, 0.089, 0.059],
                "unc":{
                    "stat":[0.004, 0.003, 0.004, 0.005, 0.009, 0.011],
                    "iso":[0.013, 0.007, 0.001, 0.040, 0.101, 0.009],
                    "closure":[0.275, 0.229, 0.031, 0.011, 0.708, 0.040],
                    "mc":[0.028, 0.036, 0.040, 0.062, 0.065, 0.086],
                }
            }
        }


    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fake_photon_weight",  "F")
        for _unc in self.unc_list:
            for _suffix in ['up', 'down']:
                self.out.branch('fake_photon_weight_{_unc}_{_suffix}'.format(_unc=_unc, _suffix=_suffix), 'F')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def calweight(self, pt, eta):
        weight = 1.
        weight_unc = {}
        for _unc in self.unc_list:
            weight_unc[_unc] = {}
            for _suffix in ['up', 'down']:
                weight_unc[_unc][_suffix] = 1.

        if abs(eta) < 1.4442:
            for i in range(0, len(self.barrel_pt_map[self.year]['ptbins'])-1):
                pt_low = self.barrel_pt_map[self.year]['ptbins'][i]
                pt_high = self.barrel_pt_map[self.year]['ptbins'][i+1]
                if (pt >= pt_low) and (pt <= pt_high):
                    weight = self.barrel_pt_map[self.year]['weight'][i]
                    for unc in weight_unc:
                        if unc == 'stat':
                            weight_unc[unc]['up'] = self.barrel_pt_map[self.year]['weight'][i] + self.barrel_pt_map[self.year]['unc'][unc][i]
                            weight_unc[unc]['down'] = max(self.barrel_pt_map[self.year]['weight'][i] - self.barrel_pt_map[self.year]['unc'][unc][i], 0)
                        else:
                            weight_unc[unc]['up'] = self.barrel_pt_map[self.year]['weight'][i] + self.barrel_pt_map[self.year]['unc'][unc][i]*self.barrel_pt_map[self.year]['weight'][i]
                            weight_unc[unc]['down'] = max(self.barrel_pt_map[self.year]['weight'][i] - self.barrel_pt_map[self.year]['unc'][unc][i]*self.barrel_pt_map[self.year]['weight'][i], 0)

        elif (abs(eta) > 1.566) and (abs(eta) < 2.5):
            for i in range(0, len(self.endcap_pt_map[self.year]['ptbins'])-1):
                pt_low = self.endcap_pt_map[self.year]['ptbins'][i]
                pt_high = self.endcap_pt_map[self.year]['ptbins'][i+1]
                if (pt >= pt_low) and (pt <= pt_high):
                    weight = self.endcap_pt_map[self.year]['weight'][i]
                    for unc in weight_unc:
                        if unc == 'stat':
                            weight_unc[unc]['up'] = self.endcap_pt_map[self.year]['weight'][i] + self.endcap_pt_map[self.year]['unc'][unc][i]
                            weight_unc[unc]['down'] = max(self.endcap_pt_map[self.year]['weight'][i] - self.endcap_pt_map[self.year]['unc'][unc][i], 0)
                        else:
                            weight_unc[unc]['up'] = self.endcap_pt_map[self.year]['weight'][i] + self.endcap_pt_map[self.year]['unc'][unc][i]*self.endcap_pt_map[self.year]['weight'][i]
                            weight_unc[unc]['down'] = max(self.endcap_pt_map[self.year]['weight'][i] - self.endcap_pt_map[self.year]['unc'][unc][i]*self.endcap_pt_map[self.year]['weight'][i], 0)

        return weight, weight_unc

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        weight = 1.
        weight_unc = {}
        for _unc in self.unc_list:
            weight_unc[_unc] = {}
            for _suffix in ['up', 'down']:
                weight_unc[_unc][_suffix] = 1.
        if event.region_mark == 3:
            if event.channel_mark in [1,2,3,4]:
                weight, weight_unc = self.calweight(event.WZG_photon_pt, event.WZG_photon_eta) 
            elif event.channel_mark in [31,32]:
                weight, weight_unc = self.calweight(event.ZGJ_photon_pt, event.ZGJ_photon_eta) 
            elif event.channel_mark in [21,22,23,24]:
                weight, weight_unc = self.calweight(event.ttG_photon_pt, event.ttG_photon_eta) 

        self.out.fillBranch("fake_photon_weight", weight)
        for _unc in self.unc_list:
            for _suffix in ['up', 'down']:
                self.out.fillBranch('fake_photon_weight_{_unc}_{_suffix}'.format(_unc=_unc, _suffix=_suffix), weight_unc[_unc][_suffix])
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ApplyWeightFakePhotonModule = lambda : ApplyWeightFakePhotonProducer()
ApplyWeightFakePhotonModule18 = lambda : ApplyWeightFakePhotonProducer('2018')
ApplyWeightFakePhotonModule17 = lambda : ApplyWeightFakePhotonProducer('2017')
ApplyWeightFakePhotonModule16 = lambda : ApplyWeightFakePhotonProducer('2016')