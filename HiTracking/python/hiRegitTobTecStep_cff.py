import FWCore.ParameterSet.Config as cms

################################################################################### 
# pp iterative tracking modified for hiOffline reco (the vertex is the one reconstructed in HI)
################################### 3rd step: low-pT and displaced tracks from pixel triplets

from RecoHI.HiTracking.HITrackingRegionProducer_cfi import *

###################################
from RecoTracker.IterativeTracking.TobTecStep_cff import *

# NEW CLUSTERS (remove previously used clusters)
hiRegitTobTecStepClusters = cms.EDProducer("TrackClusterRemover",
                                                clusterLessSolution= cms.bool(True),
                                                oldClusterRemovalInfo = cms.InputTag("hiRegitPixelLessStepClusters"),
                                                trajectories = cms.InputTag("hiRegitPixelLessStepTracks"),
                                                overrideTrkQuals = cms.InputTag('hiRegitPixelLessStepSelector','hiRegitPixelLessStep'),
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
hiRegitTobTecStepSeedLayers =  RecoTracker.IterativeTracking.TobTecStep_cff.tobTecStepSeedLayers.clone(
    ComponentName = 'hiRegitTobTecStepSeedLayers'
    )
hiRegitTobTecStepSeedLayers.TOB.skipClusters = cms.InputTag('hiRegitTobTecStepClusters')
hiRegitTobTecStepSeedLayers.TEC.skipClusters = cms.InputTag('hiRegitTobTecStepClusters')

# seeding
hiRegitTobTecStepSeeds     = RecoTracker.IterativeTracking.TobTecStep_cff.tobTecStepSeeds.clone()
hiRegitTobTecStepSeeds.RegionFactoryPSet                                           = HiTrackingRegionFactoryFromJetsBlock.clone()
hiRegitTobTecStepSeeds.ClusterCheckPSet.doClusterCheck                             = False # do not check for max number of clusters pixel or strips
hiRegitTobTecStepSeeds.OrderedHitsFactoryPSet.SeedingLayers = 'hiRegitTobTecStepSeedLayers'
from RecoPixelVertexing.PixelLowPtUtilities.ClusterShapeHitFilterESProducer_cfi import *
#hiRegitDetachedTripletStepSeeds.OrderedHitsFactoryPSet.GeneratorPSet.SeedComparitorPSet.ComponentName = 'LowPtClusterShapeSeedComparitor'
hiRegitTobTecStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 1.7

# building: feed the new-named seeds
hiRegitTobTecStepTrajectoryFilter = RecoTracker.IterativeTracking.TobTecStep_cff.tobTecStepTrajectoryFilter.clone(
    ComponentName    = 'hiRegitTobTecStepTrajectoryFilter'
    )

hiRegitTobTecStepTrajectoryBuilder = RecoTracker.IterativeTracking.TobTecStep_cff.tobTecStepTrajectoryBuilder.clone(
    ComponentName        = 'hiRegitTobTecStepTrajectoryBuilder',
    trajectoryFilterName = 'hiRegitTobTecStepTrajectoryFilter',
    clustersToSkip       = cms.InputTag('hiRegitTobTecStepClusters')
)

hiRegitTobTecStepTrackCandidates        =  RecoTracker.IterativeTracking.TobTecStep_cff.tobTecStepTrackCandidates.clone(
    src               = cms.InputTag('hiRegitTobTecStepSeeds'),
    TrajectoryBuilder = 'hiRegitTobTecStepTrajectoryBuilder',
    maxNSeeds=100000
    )

# fitting: feed new-names
hiRegitTobTecStepTracks                 = RecoTracker.IterativeTracking.TobTecStep_cff.tobTecStepTracks.clone(
    src                 = 'hiRegitTobTecStepTrackCandidates',
    #AlgorithmName = cms.string('iter10'),
    AlgorithmName = cms.string('iter6'),
    )


# Track selection
import RecoHI.HiTracking.hiMultiTrackSelector_cfi
hiRegitTobTecStepSelector = RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiMultiTrackSelector.clone(
    src='hiRegitTobTecStepTracks',
    trackSelectors= cms.VPSet(
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiLooseMTS.clone(
    name = 'hiRegitTobTecStepLoose',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ), #end of pset
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiTightMTS.clone(
    name = 'hiRegitTobTecStepTight',
    preFilterName = 'hiRegitTobTecStepLoose',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ),
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiHighpurityMTS.clone(
    name = 'hiRegitTobTecStep',
    preFilterName = 'hiRegitTobTecStepTight',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ),
    ) #end of vpset
    ) #end of clone  


hiRegitTobTecStep = cms.Sequence(hiRegitTobTecStepClusters*
                                          hiRegitTobTecStepSeeds*
                                          hiRegitTobTecStepTrackCandidates*
                                          hiRegitTobTecStepTracks*
                                          hiRegitTobTecStepSelector
                                          )
