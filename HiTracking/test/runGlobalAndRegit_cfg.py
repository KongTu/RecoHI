#import FWCore.ParameterSet.VarParsing as VarParsing

#ivars = VarParsing.VarParsing('standard')
#ivars.register('initialEvent',mult=ivars.multiplicity.singleton,info="for testing")

#ivars.files = 'file:/mnt/hadoop/cms/store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/00B2685E-F075-E211-B6F7-0024E86E8D3F.root'
#ivars.files = 'root://xrootd1.cmsaf.mit.edu//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/00B2685E-F075-E211-B6F7-0024E86E8D3F.root','root://xrootd1.cmsaf.mit.edu//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/003BB1BC-E875-E211-9EB4-00266CF9BEF8.root','root://xrootd1.cmsaf.mit.edu//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/00B2685E-F075-E211-B6F7-0024E86E8D3F.root','root://xrootd1.cmsaf.mit.edu//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/06920E6B-EE75-E211-84AE-008CFA00148C.root','root://xrootd1.cmsaf.mit.edu//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/0A62EB3F-F575-E211-BFA6-0026B94E2817.root'

#ivars.files = 'root://xrootd.ba.infn.it//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_2p76TeV_pythia6/GEN-SIM-RECO/STARTHI53_V28-v1/00000/024EE17E-A47A-E311-8982-7845C4FC3A1C.root'
#ivars.output = 'test.root'
#ivars.maxEvents = -1
#ivars.initialEvent = 1

#ivars.parseArguments()

import FWCore.ParameterSet.Config as cms

process = cms.Process('TRACKATTACK')

doRegit=True
rawORreco=True
isEmbedded=True

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring('root://xrootd1.cmsaf.mit.edu//store/himc/HiWinter13/QCD_Pt_80_TuneZ2_5p02TeV/GEN-SIM-RECO/pp_STARTHI53_V25-v1/20000/00B2685E-F075-E211-B6F7-0024E86E8D3F.root')
)

process.Timing = cms.Service("Timing")

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32(100))


#####################################################################################
# Load some general stuff
#####################################################################################

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('RecoLocalTracker.SiPixelRecHits.PixelCPEESProducers_cff')
# Data Global Tag 44x 
#process.GlobalTag.globaltag = 'GR_P_V27::All'

# MC Global Tag 53x: 
process.GlobalTag.globaltag = 'STARTHI53_LV1::All'

# load centrality
#from CmsHi.Analysis2010.CommonFunctions_cff import *
#overrideCentrality(process)
#process.HeavyIonGlobalParameters = cms.PSet(
#	centralityVariable = cms.string("HFhits"),
#	nonDefaultGlauberModel = cms.string("Hydjet_2760GeV"),
#	centralitySrc = cms.InputTag("hiCentrality")
#	)

#process.hiCentrality.pixelBarrelOnly = False

#process.load("RecoHI.HiCentralityAlgos.CentralityFilter_cfi")
#process.centralityFilter.selectedBins = [0,1]

# EcalSeverityLevel ES Producer
process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")
process.load("RecoEcal.EgammaCoreTools.EcalNextToDeadChannelESProducer_cff")


#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                  fileName=cms.string('test.root'))

#####################################################################################
# Additional Reconstruction 
#####################################################################################

#process.load("RiceHIG.V0Analysis.v0selector_cff")
process.load("RecoVertex.V0Producer.generalV0Candidates_cff")
process.generalV0CandidatesHI = process.generalV0Candidates.clone (
    tkNhitsCut = cms.int32(0),
    tkChi2Cut = cms.double(7.0),
    dauTransImpactSigCut = cms.double(1.0),
    dauLongImpactSigCut = cms.double(1.0),
    xiVtxSignificance3DCut = cms.double(0.0),
    xiVtxSignificance2DCut = cms.double(0.0),
    vtxSignificance2DCut = cms.double(0.0),
    vtxSignificance3DCut = cms.double(4.0)
)
process.generalV0CandidatesNew = process.generalV0Candidates.clone ()
#process.selectV0CandidatesNewlambda.v0CollName = cms.string("generalV0CandidatesNew")
#process.selectV0CandidatesNewkshort.v0CollName = cms.string("generalV0CandidatesNew")


process.load("V0Analyzer.V0Analyzer.v0analyzer_cff")

process.v0analyzerNew = process.ana.clone(

  generalV0_ks = cms.InputTag("generalV0CandidatesNew:Kshort"),
  generalV0_la = cms.InputTag("generalV0CandidatesNew:Lambda"),
 # jetSrc = cms.InputTag("iterativeCone5CaloJets")
)

process.v0analyzerHI = process.ana.clone(

  generalV0_ks = cms.InputTag("generalV0CandidatesHI:Kshort"),
  generalV0_la = cms.InputTag("generalV0CandidatesHI:Lambda"),

)
# redo reco or just tracking

if rawORreco:
    process.rechits = cms.Sequence(process.siPixelRecHits * process.siStripMatchedRecHits)
    process.hiTrackReco = cms.Sequence(process.rechits * process.hiTracking)


    process.trackRecoAndSelection = cms.Path(
        #process.centralityFilter*
        process.hiTrackReco 
        )
    
else:
    process.reco_extra = cms.Path(
        #process.centralityFilter *
        process.RawToDigi * process.reconstructionHeavyIons)
    

    
# tack on iteative tracking, particle flow and calo-matching

#iteerative tracking
#process.load("RecoHI.HiTracking.hiIterTracking_cff")
#process.hiTracking *= process.hiIterTracking


# Now do more tracking around the jets

if doRegit:
    process.load("RecoHI.HiTracking.hiRegitTracking_cff")
    
    process.hiRegitInitialStepSeeds.RegionFactoryPSet.RegionPSet.JetSrc = cms.InputTag("iterativeCone5CaloJets")
    process.hiRegitLowPtTripletStepSeeds.RegionFactoryPSet.RegionPSet.JetSrc = cms.InputTag("iterativeCone5CaloJets")
    process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.JetSrc = cms.InputTag("iterativeCone5CaloJets")
    process.hiRegitDetachedTripletStepSeeds.RegionFactoryPSet.RegionPSet.JetSrc = cms.InputTag("iterativeCone5CaloJets")
    process.hiRegitMixedTripletStepSeedsA.RegionFactoryPSet.RegionPSet.JetSrc = cms.InputTag("iterativeCone5CaloJets")
    process.hiRegitMixedTripletStepSeedsB.RegionFactoryPSet.RegionPSet.JetSrc = cms.InputTag("iterativeCone5CaloJets")
    

#pp pT cuts on all steps:
#HI pT cuts are higher than these

    process.hiRegitInitialStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 0.6
    process.hiRegitLowPtTripletStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 0.2
    process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 0.2
    process.hiRegitDetachedTripletStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 0.3
    process.hiRegitMixedTripletStepSeedsA.RegionFactoryPSet.RegionPSet.ptMin = 0.4
    process.hiRegitMixedTripletStepSeedsB.RegionFactoryPSet.RegionPSet.ptMin = 0.6

#original radius or halfLength radius:

    #custom regit settings not yet in release
    process.hiRegitInitialStepSeeds.RegionFactoryPSet.RegionPSet.originRadius = 0.02
    process.hiRegitLowPtTripletStepSeeds.RegionFactoryPSet.RegionPSet.originRadius = 0.02
    #process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.originRadius = 0.02
    process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.originRadius = 0.015 # new pp setting
    process.hiRegitDetachedTripletStepSeeds.RegionFactoryPSet.RegionPSet.originRadius = 1.5
    process.hiRegitMixedTripletStepSeedsA.RegionFactoryPSet.RegionPSet.originRadius = 0.5 #pp settings: 1.5
    process.hiRegitMixedTripletStepSeedsB.RegionFactoryPSet.RegionPSet.originRadius = 0.5 #pp settings: 1.5

    process.hiRegitInitialStepSeeds.RegionFactoryPSet.RegionPSet.originHalfLength = 0.02
    process.hiRegitLowPtTripletStepSeeds.RegionFactoryPSet.RegionPSet.originHalfLength = 0.02
    #process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.originHalfLength = 0.02
    process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.originHalfLength = 0.015 # new pp setting
    process.hiRegitDetachedTripletStepSeeds.RegionFactoryPSet.RegionPSet.originHalfLength = 1.5 #pp is 15
    process.hiRegitMixedTripletStepSeedsA.RegionFactoryPSet.RegionPSet.originHalfLength = 0.5 #pp is 10
    process.hiRegitMixedTripletStepSeedsB.RegionFactoryPSet.RegionPSet.originHalfLength = 0.5 #pp is 10

## in pp tracking the deltaeta deltaPhi is 0.1, but in HI reigit:

    process.hiRegitInitialStepSeeds.RegionFactoryPSet.RegionPSet.deltaPhiRegion = 0.3
    process.hiRegitInitialStepSeeds.RegionFactoryPSet.RegionPSet.deltaEtaRegion = 0.3
    process.hiRegitLowPtTripletStepSeeds.RegionFactoryPSet.RegionPSet.deltaPhiRegion = 0.3
    process.hiRegitLowPtTripletStepSeeds.RegionFactoryPSet.RegionPSet.deltaEtaRegion = 0.3
    process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.deltaPhiRegion = 0.3
    process.hiRegitPixelPairStepSeeds.RegionFactoryPSet.RegionPSet.deltaEtaRegion = 0.3
    process.hiRegitDetachedTripletStepSeeds.RegionFactoryPSet.RegionPSet.deltaPhiRegion = 0.3
    process.hiRegitDetachedTripletStepSeeds.RegionFactoryPSet.RegionPSet.deltaEtaRegion = 0.3
    process.hiRegitMixedTripletStepSeedsA.RegionFactoryPSet.RegionPSet.deltaPhiRegion = 0.3
    process.hiRegitMixedTripletStepSeedsA.RegionFactoryPSet.RegionPSet.deltaEtaRegion = 0.3
    process.hiRegitMixedTripletStepSeedsB.RegionFactoryPSet.RegionPSet.deltaPhiRegion = 0.3
    process.hiRegitMixedTripletStepSeedsB.RegionFactoryPSet.RegionPSet.deltaEtaRegion = 0.3

    # merged with the global, iterative tracking
    process.load("RecoHI.HiTracking.MergeRegit_cff")


    
    # now re-run the muons
    process.regGlobalMuons = process.globalMuons.clone(
        TrackerCollectionLabel = "hiGeneralAndRegitTracks"
        )
    process.regGlbTrackQual = process.glbTrackQual.clone(
        InputCollection = "regGlobalMuons",
        InputLinksCollection = "regGlobalMuons"
        )
    process.regMuons = process.muons.clone()
    process.regMuons.TrackExtractorPSet.inputTrackCollection = "hiGeneralAndRegitTracks"
    process.regMuons.globalTrackQualityInputTag = "regGlbTrackQual"
    process.regMuons.inputCollectionLabels = cms.VInputTag("hiGeneralAndRegitTracks", "regGlobalMuons", "standAloneMuons:UpdatedAtVtx", "tevMuons:firstHit", "tevMuons:picky",
                                                           "tevMuons:dyt")
    
    
    process.regMuonReco = cms.Sequence(
        process.regGlobalMuons*
        process.regGlbTrackQual*
        process.regMuons
        )
    
    process.regionalTracking = cms.Path(
        process.hiRegitTracking *
        process.hiGeneralAndRegitTracks
#        process.regMuonReco 
        )
    
if doRegit:
    process.generalV0CandidatesHI.trackRecoAlgorithm = 'hiGeneralAndRegitTracks'
else:
    process.generalV0CandidatesHI.trackRecoAlgorithm = 'hiGeneralTracks'
    
process.V0_step = cms.Path(
    process.generalV0CandidatesHI +
    process.generalV0CandidatesNew +
    process.v0analyzerNew +
    process.v0analyzerHI
     
)

#process.load("edwenger.HiTrkEffAnalyzer.HiTPCuts_cff")
#process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
#process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")
#process.load("MitHig.PixelTrackletAnalyzer.trackAnalyzer_cff")
#process.cutsTPForEff.primaryOnly = False
#process.cutsTPForFak.ptMin = 0.2
#process.cutsTPForEff.ptMin = 0.2

#if doRegit:
#    process.anaTrack.trackSrc = 'hiGeneralAndRegitTracks'
#    process.anaTrack.qualityString = "highPurity"
#else:
#    process.anaTrack.trackSrc = 'hiGeneralTracks'
#    process.anaTrack.qualityString = "highPurity"

#process.anaTrack.trackPtMin = 0
#process.anaTrack.useQuality = False
#process.anaTrack.doPFMatching = False
#process.anaTrack.doSimTrack = True    

#process.trackAnalysis = cms.Path(
#    process.cutsTPForEff*
#    process.cutsTPForFak*
#    process.anaTrack
#    )


#####################################################################################
# Edm Output
#####################################################################################

#process.out = cms.OutputModule("PoolOutputModule",
 #                              fileName = cms.untracked.string("output.root")
  #                             )
#process.save = cms.EndPath(process.out)
