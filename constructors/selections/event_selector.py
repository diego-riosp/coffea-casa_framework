import numpy as np
import awkward as ak
from coffea.analysis_tools import PackedSelection
from loadmodule import loadModule
UtilFunctions = loadModule("constructors/utils/util_functions.py")
uf = UtilFunctions()

class EventSelector:
    def __init__(self, events, year, lumi_info):
        self.events = events
        self.year = year
        self.lumi_info = lumi_info
        
    def selectEvents(self, muons, objects, mass):        
        events = self.events
        year = self.year
        selections = PackedSelection()
        selections.add("golden_json", uf.goldenJson(events, year, self.lumi_info))
        selections.add("npvsGood", events.PV.npvsGood>0)
        selections.add("IsoMu24", events.HLT.IsoMu24)
        selections.add("two_muons", ak.num(muons)==2)
        selections.add("one_dimuon", ak.num(objects)==1)
        selections.add("leading_muon_pt", ak.firsts(muons.pt) > 30)
        selections.add("subleading_muon_pt", ak.pad_none(muons, target=2)[:, 1].pt > 15)
        region_mask = selections.all("golden_json","npvsGood","IsoMu24", "two_muons", 
                                     "one_dimuon", "leading_muon_pt", "subleading_muon_pt")
        pruned_ev = events[region_mask]
        pruned_mass = mass[region_mask]
        return (pruned_ev, pruned_mass)