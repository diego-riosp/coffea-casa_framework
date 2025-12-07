import awkward as ak
import numpy as np
class ObjectSelector:
    
    def __init__(self, events):
        self.events = events
        
    def muonSelector(self):
        events = self.events
        muons = events.Muon
        good_muons = (
            (muons.pt > 35)
            & (abs(muons.eta) < 2.4)
            & muons.tightId
            & (muons.pfRelIso03_all < 0.15)
        )
        muons = muons[good_muons]
        
        dimuons = ak.combinations(muons, 2, fields=["lead","trail"])
        dimuons = dimuons[dimuons.lead.charge != dimuons.trail.charge]
        mass = ak.firsts((dimuons.lead + dimuons.trail).mass)
        mass = ak.nan_to_num(mass, nan=0)
        return (dimuons, mass)