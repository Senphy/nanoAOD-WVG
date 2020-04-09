import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/afs/cern.ch/work/s/sdeng/config_file/genproductions/bin/MadGraph5_aMCatNLO/WZAToLNuLLA_4f_NLO_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

#Link to datacards:
#https://github.com/cms-sw/genproductions/tree/95b7020736bb624b56a542785470193d4f63cb85/bin/MadGraph5_aMCatNLO/cards/production/13TeV/WVAToLNu2jA_VisWorZ_4f_NLO