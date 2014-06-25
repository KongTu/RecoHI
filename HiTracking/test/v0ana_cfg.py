import FWCore.ParameterSet.Config as cms

process = cms.Process('V0ANA')

#global tag:

gTag = 'STARTHI53_LV1::All'

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

### standard includes
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.HiGenCommon.VtxSmearedRealisticPPbBoost8TeVCollision_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load("Configuration.StandardSequences.Digi_cff")
process.load("Configuration.StandardSequences.DigiToRaw_cff")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("SimGeneral.MixingModule.mixNoPU_cfi")
process.load("SimGeneral.TrackingAnalysis.trackingParticles_cfi")


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( -1 )
)

# Input source
process.source = cms.Source("PoolSource",
                            secondaryFileNames = cms.untracked.vstring(
    #'/store/user/mnguyen/Pyquen_BJet_Pt80_TuneZ2_Unquenched_Hydjet1p8_2760GeV/hiRECO_bJet80_v2/296b762a3f7ae585942f7234457ce1af/hiReco_RAW2DIGI_L1Reco_RECO_5_1_rAn.root'
    #'/store/user/mnguyen/bJet_2760GeV_Pt80_RAW_v7/hiRECO_bJet80_signal_v7/ccf75564b83bb55ba9072adf72403ec5/hiReco_RAW2DIGI_L1Reco_RECO_29_1_Jj2.root'
    #'file:./allOut.root'
    #'file:./hiReco_RAW2DIGI_L1Reco_RECO_9_1_sqN.root'
    '/store/user/mnguyen/Pyquen_BJet_Pt80_TuneZ2_Unquenched_Hydjet1p8_2760GeV/hiRECO_bJet80_v2/296b762a3f7ae585942f7234457ce1af/hiReco_RAW2DIGI_L1Reco_RECO_5_1_rAn.root'
    ),
                            fileNames = cms.untracked.vstring(
    #'/store/user/mnguyen/Pyquen_BJet_Pt80_TuneZ2_Unquenched_Hydjet1p8_2760GeV//hiREGIT_bJet80_v2/25b9987835d96d453a51d7ce5afb3b54/regionalTracking_1_1_NJG.root'
    #'/store/user/mnguyen/bJet_2760GeV_Pt80_RAW_v7/hiREGIT_bJet80_signal_v7/8b3aa948f4d16b56ded5687e096a54bb/regionalTracking_29_1_kJy.root'
    #'file:./regionalTracking.root'
    '/store/user/mnguyen/Pyquen_BJet_Pt80_TuneZ2_Unquenched_Hydjet1p8_2760GeV/hiREGIT_akPu3PF_ppSettings_bJet80_v2/f54c784c380faf301b95a6245110e62c/regionalTracking_1_1_oeP.root'
    ),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                            #eventsToProcess = cms.untracked.VEventRange('1:337-1:337'),
                            #lumisToProcess = cms.untracked.VLuminosityBlockRange('1:19-1:19'),
                            )

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# Additional output definition

# Other statements
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = gTag

print "global Tag = ", process.GlobalTag.globaltag     

# load V0Producer, V0selector, V0Analyzer
process.load("RecoVertex.V0Producer.generalV0Candidates_cff")
process.load("RiceHIG.V0Analysis.v0selector_cff")
process.load("RiceHIG.V0Analysis.v0validator_cff")
process.load("V0Analyzer.V0Analyzer.v0analyzer_cff")

process.generalV0CandidatesNew = process.generalV0Candidates.clone (
    tkNhitsCut = cms.int32(0),
    tkChi2Cut = cms.double(7.0),
    dauTransImpactSigCut = cms.double(1.0),
    dauLongImpactSigCut = cms.double(1.0),
    xiVtxSignificance3DCut = cms.double(0.0),
    xiVtxSignificance2DCut = cms.double(0.0),
    vtxSignificance2DCut = cms.double(0.0),
    vtxSignificance3DCut = cms.double(4.0),
    trackRecoAlgorithm = cms.InputTag('hiRegitTracks') 
)

process.ana.generalV0_ks = cms.InputTag('selectV0CandidatesNewkshort:Kshort')
process.ana.generalV0_la = cms.InputTag('selectV0CandidatesNewlambda:Lambda')
process.ana.doPFJet = cms.untracked.bool(False)
process.ana.doGenJet = cms.untracked.bool(False)
process.ana.doCaloJet = cms.untracked.bool(False)
process.ana.doGenParticle = cms.untracked.bool(False)
process.ana.trackSrc = cms.InputTag('hiRegitTracks')

process.selectV0CandidatesNewlambda.v0CollName = cms.string("generalV0CandidatesNew")
process.selectV0CandidatesNewkshort.v0CollName = cms.string("generalV0CandidatesNew")



#output file name:

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(
    'globalAnaRegionalAna.root'
    #'doubleRegitTest.root'
    )
                                   )

process.v0ana = cms.Sequence(process.generalV0CandidatesNew*process.selectV0CandidatesNewlambda*process.selectV0CandidatesNewkshort*process.ana)

process.ana_step = cms.Path(process.v0ana)

