import os,sys
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms

lumisToProcess = cms.untracked.VLuminosityBlockRange( LumiList.LumiList(filename="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt").getCMSSWString().split(',') )
# print lumisToProcess

runsAndLumis = {}
for l in lumisToProcess:
    if "-" in l:
        start, stop = l.split("-")
        rstart, lstart = start.split(":")
        rstop, lstop = stop.split(":")
    else:
        rstart, lstart = l.split(":")
        rstop, lstop = l.split(":")
    if rstart != rstop:
        raise Exception(
            "Cannot convert '%s' to runs and lumis json format" % l)
    if rstart not in runsAndLumis:
        runsAndLumis[rstart] = []
    runsAndLumis[rstart].append([int(lstart), int(lstop)])
print runsAndLumis