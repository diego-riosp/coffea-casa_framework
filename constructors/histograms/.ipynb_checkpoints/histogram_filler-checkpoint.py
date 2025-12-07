import awkward as ak
import hist

class HistogramFiller:
    def __init__(self, events):
        self.events = events
    def fillHistogram(self,region_weights,pruned_mass):
        events = self.events
        dataset = events.metadata["dataset"]
        weights = ak.broadcast_arrays(region_weights, pruned_mass)[0]
        sumw_before = ak.sum(events.genWeight)
        sumw_after = ak.sum(region_weights)
        dimuon_mass_hist = hist.Hist.new.Reg(30, 60, 120, name="mass", label="mμμ [GeV]").Weight()
        dimuon_mass_hist.fill(
            mass=ak.to_numpy(pruned_mass),
            weight=ak.to_numpy(weights),
        )
        L = 41477.88
        xs = 3503.7
        dimuon_mass_hist = dimuon_mass_hist * L*xs*sumw_after/sumw_before
        histograms = {
            "entries": ak.num(events, axis=0),
            "mass": dimuon_mass_hist,
        }
        return histograms