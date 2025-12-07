import awkward as ak
from coffea.analysis_tools import PackedSelection

class EventSelector:
    def __init__(self, events):
        self.events = events
    def selectEvents(self, objects, mass):
        events = self.events
        selections = PackedSelection()
        selections.add("IsoMu24", events.HLT.IsoMu24)
        selections.add("at_least_one_dimuons", ak.num(objects)>0)
        region_mask = selections.all("IsoMu24", "at_least_one_dimuons")
        pruned_ev = events[region_mask]
        mass = mass[region_mask]
        return (pruned_ev, mass)
        