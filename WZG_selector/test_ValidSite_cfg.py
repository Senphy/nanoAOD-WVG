import sys,os
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')
options.parseArguments()

process = cms.Process("Test")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.source = cms.Source ("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)
