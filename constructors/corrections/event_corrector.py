import correctionlib
import awkward as ak
import numpy as np
from coffea.analysis_tools import Weights

class EventCorrector:
    def __init__(self, pruned_ev, corr_id, corr_iso, corr_trg):
        self.pruned_ev = pruned_ev
        self.corr_id = corr_id
        self.corr_iso = corr_iso
        self.corr_trg = corr_trg
        
    def _compute_sf(self, corr, objects_eta, objects_pt, objects_mask, n, syst):
        sf = corr.evaluate(objects_eta, objects_pt, syst)
        sf = ak.where(objects_mask, sf, ak.ones_like(sf))
        sf = ak.unflatten(sf, n)
        return ak.prod(sf, axis=1)


    def scaleFactors(self, syst: str = "nominal"):
        pruned_ev = self.pruned_ev
    
        is_mc = "genWeight" in pruned_ev.fields
        if not is_mc:
            return ak.ones_like(pruned_ev.event)
    
        muons = pruned_ev.Muon
        m, n = ak.flatten(muons), ak.num(muons)
    
        objects_mask = (m.pt > 26.01) & (np.abs(m.eta) < 2.39)
        in_limit_objects = m.mask[objects_mask]
    
        objects_pt = ak.fill_none(in_limit_objects.pt, 26.01)
        objects_eta = ak.fill_none(np.abs(in_limit_objects.eta), 0.)
    
        sf_id  = self._compute_sf(self.corr_id,  objects_eta, objects_pt, objects_mask, n, syst)
        sf_iso = self._compute_sf(self.corr_iso, objects_eta, objects_pt, objects_mask, n, syst)
        sf_trg = self._compute_sf(self.corr_trg, objects_eta, objects_pt, objects_mask, n, syst)
    
        weights = Weights(size=len(pruned_ev), storeIndividual=True)
        weights.add("sf_id", sf_id)
        weights.add("sf_iso", sf_iso)
        weights.add("sf_trg", sf_trg)
    
        return weights.weight()





        