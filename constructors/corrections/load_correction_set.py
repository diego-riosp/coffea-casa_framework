import correctionlib

class LoadCorrectionSet():
    def __init__(self, year, corr_dict):
        self.year = year
        events = corr_dict["muons"]["events"]

        for key, file_dict in events.items():
            json_path, cname = next(iter(file_dict.items()))
            cset = correctionlib.CorrectionSet.from_file(json_path)
            setattr(self, f"{key}_evcorr", cset[cname])

        objects = corr_dict["muons"].get("objects", {})
        for key, json_path in objects.items():
            cset = correctionlib.CorrectionSet.from_file(json_path)
            setattr(self, f"{key}_objcorr", cset)
            
    def printer(self):

        print("=== corrections loaded ===")
        for attr in dir(self):
            if attr.endswith("corr"):
                print(f"{attr}: {getattr(self, attr)}")