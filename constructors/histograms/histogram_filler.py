import awkward as ak
import hist
from loadmodule import loadAll
loadAll("constructors/selections/object_selector.py")
loadAll("constructors/utils/util_functions.py")

class HistogramFiller:
    def __init__(self, events, histogram, is_mc:bool, sumw):
        self.events = events
        self.histogram = histogram
        self.is_mc = is_mc
        self.sumw = sumw
    
    def fillHistogram(self, region_weights, objects):
        events = self.events
        
        if self.is_mc:
            weights = ak.broadcast_arrays(region_weights, objects["dimuons"].p4.mass)[0]
            self.histogram.fill(
                mass=ak.to_numpy(ak.flatten(objects["dimuons"].p4.mass)),
                weight=ak.to_numpy(ak.flatten(weights)),
            )
            L = 7980.4
            xsec = events.metadata["xsec"]
            scaling = (L * xsec) / self.sumw
            self.histogram *= scaling
            
        else:
            self.histogram.fill(
                mass=ak.to_numpy(ak.flatten(objects["dimuons"].p4.mass)),
                weight=ak.to_numpy(region_weights),
            )
        return self.histogram