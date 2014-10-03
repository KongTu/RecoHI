import FWCore.ParameterSet.Config as cms

################################################################################### 
# pp iterative tracking modified for hiOffline reco (the vertex is the one reconstructed in HI)
################################### 3rd step: low-pT and displaced tracks from pixel triplets

from RecoHI.HiTracking.HITrackingRegionProducer_cfi import *

###################################
from RecoTracker.IterativeTracking.PixelLessStep_cff import *

# NEW CLUSTERS (remove previously used clusters)
hiRegitPixelLessStepClusters = cms.EDProducer("TrackClusterRemover",
                                                clusterLessSolution= cms.bool(True),
                                                oldClusterRemovalInfo = cms.InputTag("hiRegitMixedTripletStepClusters"),
                                                trajectories = cms.InputTag("hiRegitMixedTripletStepTracks"),
                                                overrideTrkQuals = cms.InputTag('hiRegitMixedTripletStepSelector','hiRegitMixedTripletStep'),
                                                TrackQuality = cms.string('highPurity'),
                                                pixelClusters = cms.InputTag("siPixelClusters"),
                                                stripClusters = cms.InputTag("siStripClusters"),
                                                Common = cms.PSet(
    maxChi2 = cms.double(9.0),
    ),
                                                Strip = cms.PSet(
    maxChi2 = cms.double(9.0),
    #Yen-Jie's mod to preserve merged clusters
    maxSize = cms.uint32(2)
    )
                                                )



# SEEDING LAYERS
hiRegitPixelLessStepSeedLayers =  RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepSeedLayers.clone(
    ComponentName = 'hiRegitPixelLessStepSeedLayers'
    )
hiRegitPixelLessStepSeedLayers.TIB.skipClusters = cms.InputTag('hiRegitPixelLessStepClusters')
hiRegitPixelLessStepSeedLayers.TID.skipClusters = cms.InputTag('hiRegitPixelLessStepClusters')
hiRegitPixelLessStepSeedLayers.TEC.skipClusters = cms.InputTag('hiRegitPixelLessStepClusters')
# seeding
hiRegitPixelLessStepSeeds     = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepSeeds.clone()
hiRegitPixelLessStepSeeds.RegionFactoryPSet                                           = HiTrackingRegionFactoryFromJetsBlock.clone()
hiRegitPixelLessStepSeeds.ClusterCheckPSet.doClusterCheck                             = False # do not check for max number of clusters pixel or strips
hiRegitPixelLessStepSeeds.OrderedHitsFactoryPSet.SeedingLayers = 'hiRegitPixelLessStepSeedLayers'
from RecoPixelVertexing.PixelLowPtUtilities.ClusterShapeHitFilterESProducer_cfi import *
#hiRegitDetachedTripletStepSeeds.OrderedHitsFactoryPSet.GeneratorPSet.SeedComparitorPSet.ComponentName = 'LowPtClusterShapeSeedComparitor'
hiRegitPixelLessStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 1.7

# building: feed the new-named seeds
hiRegitPixelLessStepTrajectoryFilter = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTrajectoryFilter.clone(
    ComponentName    = 'hiRegitPixelLessStepTrajectoryFilter'
    )

hiRegitPixelLessStepTrajectoryBuilder = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTrajectoryBuilder.clone(
    ComponentName        = 'hiRegitPixelLessStepTrajectoryBuilder',
    trajectoryFilterName = 'hiRegitPixelLessStepTrajectoryFilter',
    clustersToSkip       = cms.InputTag('hiRegitPixelLessStepClusters')
)

hiRegitPixelLessStepTrackCandidates        =  RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTrackCandidates.clone(
    src               = cms.InputTag('hiRegitPixelLessStepSeeds'),
    TrajectoryBuilder = 'hiRegitPixelLessStepTrajectoryBuilder',
    maxNSeeds=100000
    )

# fitting: feed new-names
hiRegitPixelLessStepTracks                 = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTracks.clone(
    src                 = 'hiRegitPixelLessStepTrackCandidates',
    #AlgorithmName = cms.string('iter9'),
    AlgorithmName = cms.string('iter5'),
    )


# Track selection
import RecoHI.HiTracking.hiMultiTrackSelector_cfi
hiRegitPixelLessStepSelector = RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiMultiTrackSelector.clone(
    src='hiRegitPixelLessStepTracks',
    trackSelectors= cms.VPSet(
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiLooseMTS.clone(
    name = 'hiRegitPixelLessStepLoose',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ), #end of pset
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiTightMTS.clone(
    name = 'hiRegitPixelLessStepTight',
    preFilterName = 'hiRegitPixelLessStepLoose',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ),
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiHighpurityMTS.clone(
    name = 'hiRegitPixelLessStep',
    preFilterName = 'hiRegitPixelLessStepTight',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ),
    ) #end of vpset
    ) #end of clone  


hiRegitPixelLessStep = cms.Sequence(hiRegitPixelLessStepClusters*
                                          hiRegitPixelLessStepSeeds*
                                          hiRegitPixelLessStepTrackCandidates*
                                          hiRegitPixelLessStepTracks*
                                          hiRegitPixelLessStepSelector
                                          )
