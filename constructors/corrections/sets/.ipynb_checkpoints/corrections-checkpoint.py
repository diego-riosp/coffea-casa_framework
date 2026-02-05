def corr_dict(year):
    path = '/home/cms-jovyan/coffea-casa_framework/constructors/corrections/sets/'
    return {
        'muons': {
            'events': {
                'muon_Z_id': {
                    path + 'ScaleFactors_Muon_Z_ID_ISO_2022_schemaV2.json':
                    'NUM_TightID_DEN_TrackerMuons'
                },
                'muon_Z_iso': {
                    path + 'ScaleFactors_Muon_Z_ID_ISO_2022_schemaV2.json':
                    'NUM_TightPFIso_DEN_TightID'
                },
                'muon_Z_trg': {
                    path + 'ScaleFactors_Muon_Z_HLT_2022_abseta_pt_schemaV2.json':
                    'NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight'
                },
            },
            'objects': {
                'smearing': path + 'muon_scalesmearing.json.gz'
            }
        }
    }
