import correctionlib
#from coffea.lookup_tools import txt_converters, rochester_lookup

class LoadCorrectionSet():
    def __init__(self, year, corr_dict):
        self.year = year
        
        # ============================================================
        # EVENT CORRECTIONS (e.g. muon_Z JSON using correctionlib)
        # ============================================================
        events = corr_dict["muons"]["events"]

        for key, file_dict in events.items():
            json_path, cname = next(iter(file_dict.items()))
            cset = correctionlib.CorrectionSet.from_file(json_path)
            setattr(self, f"{key}_evcorr", cset[cname])

        # ============================================================
        # OBJECT CORRECTIONS (e.g. Rochester .txt file)
        # ============================================================

        objects = corr_dict["muons"].get("objects", {})
        for key, json_path in objects.items():
            cset = correctionlib.CorrectionSet.from_file(json_path)
            setattr(self, f"{key}_objcorr", cset)
        
        
        # #The following procedure is to be applied in Run2
        # objects = corr_dict["muons"].get("objects", {})
        
        # for key, path in objects.items():

        #     # Load Rochester data from text file
        #     roc_data = txt_converters.convert_rochester_file(
        #         path,
        #         loaduncs=True
        #     )

        #     # Build lookup function
        #     roc_corr = rochester_lookup.rochester_lookup(roc_data)

        #     # Store correction as: self.<key>_objcorr
        #     setattr(self, f"{key}_objcorr", roc_corr)

    
    # ============================================================
    # PRINTER (display all loaded corrections)
    # ============================================================
    def printer(self):

        print("=== corrections loaded ===")
        for attr in dir(self):
            if attr.endswith("corr"):
                print(f"{attr}: {getattr(self, attr)}")