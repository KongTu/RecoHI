import FWCore.ParameterSet.Config as cms

import RecoTracker.FinalTrackSelectors.trackListMerger_cfi
hiRegitTracks = RecoTracker.FinalTrackSelectors.trackListMerger_cfi.trackListMerger.clone(
    TrackProducers = (cms.InputTag('hiRegitInitialStepTracks'),
                      cms.InputTag('hiRegitLowPtTripletStepTracks'),
                      cms.InputTag('hiRegitPixelPairStepTracks'),
                      cms.InputTag('hiRegitDetachedTripletStepTracks'),
                      cms.InputTag('hiRegitMixedTripletStepTracks'),
		      cms.InputTag('hiRegitPixelLessStepTracks'),
		      cms.InputTag('hiRegitTobTecStepTracks')),
    hasSelector=cms.vint32(1,1,1,1,1,1,1),
    selectedTrackQuals = cms.VInputTag(
    cms.InputTag("hiRegitInitialStepSelector","hiRegitInitialStep"),
    cms.InputTag("hiRegitLowPtTripletStepSelector","hiRegitLowPtTripletStep"),
    cms.InputTag("hiRegitPixelPairStepSelector","hiRegitPixelPairStep"),
    cms.InputTag("hiRegitDetachedTripletStepSelector","hiRegitDetachedTripletStep"),
    cms.InputTag("hiRegitMixedTripletStepSelector","hiRegitMixedTripletStep"),
    cms.InputTag("hiRegitPixelLessStepSelector","hiRegitPixelLessStep"),
    cms.InputTag("hiRegitTobTecStepSelector","hiRegitTobTecStep"),
    ),                    
    setsToMerge = cms.VPSet( cms.PSet( tLists=cms.vint32(0,1,2,3,4,5,6,7), pQual=cms.bool(True)),  # should this be False?
                             ),
    copyExtras = True,
    makeReKeyedSeeds = cms.untracked.bool(False)
    )
