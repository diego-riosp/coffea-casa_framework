import awkward as ak
import hist

class HistogramFiller:
    def __init__(self, events, histogram):
        self.events = events
        self.histogram = histogram
    
    def fillHistogram(self, region_weights, pruned_ev, pruned_mass, xsec):
        events = self.events
        if xsec is not None:
            weights = ak.broadcast_arrays(region_weights, pruned_mass)[0]
            self.histogram.fill(
                mass=ak.to_numpy(pruned_mass),
                weight=ak.to_numpy(weights),
            )
            sumw_before = ak.sum(events.genWeight)
            sumw_after = ak.sum(region_weights)
            L = 7980.4
            scaling = (L * xsec) * sumw_after / sumw_before
            self.histogram *= scaling
            
        else:
            self.histogram.fill(
                mass=ak.to_numpy(pruned_mass),
                weight=ak.to_numpy(ak.ones_like(pruned_ev.event)),
            )
        return self.histogram

# class HistogramFiller:
#     def __init__(self, events, histograms):
#         self.events = events
#         self.histograms = histograms
    
#     @staticmethod
#     def empty():
#         return hist.Hist.new.Reg(
#             30, 60, 120,
#             name="mass",
#             label="mμμ [GeV]"
#         ).Weight()
    
#     def fillHistogram(self, region_weights, pruned_mass, xsec):
#         events = self.events
#         dataset = events.metadata["dataset"]
#         weights = ak.broadcast_arrays(region_weights, pruned_mass)[0]
#         is_mc = hasattr(events, "genWeight") and events.genWeight is not None
#         if is_mc:
#             sumw_before = ak.sum(events.genWeight)
#         else:
#             sumw_before = len(events)
#         sumw_after = ak.sum(region_weights)
#         #dimuon_mass_hist = hist.Hist.new.Reg(30, 60, 120, name="mass", label="mμμ [GeV]").Weight()
#         dimuon_mass_hist = self.histograms
#         dimuon_mass_hist.fill(
#             mass=ak.to_numpy(pruned_mass),
#             weight=ak.to_numpy(weights),
#         )
#         if is_mc:
#             L = 7980.4
#             #dimuon_mass_hist = dimuon_mass_hist * L * xsec * sumw_after / sumw_before
#             dimuon_mass_hist = dimuon_mass_hist * L * xsec / sumw_before
#         histograms = {
#             #"entries": ak.num(events, axis=0),
#             "mass": dimuon_mass_hist,
#         }
#         return histograms