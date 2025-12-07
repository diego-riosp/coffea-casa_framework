import correctionlib
import awkward as ak
import numpy as np
from coffea.analysis_tools import Weights

class EventCorrector:
    def __init__(self, pruned_ev, corr):
        self.pruned_ev = pruned_ev
        self.corr = corr
        
    # def correctionsExplorer(self):
    #     for i, corr in enumerate(data["corrections"]):
    #         if corr["name"] == "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight":
    #             print(json.dumps(corr, indent=2))
    #             break
    #     return 0

    def scaleFactors(self, syst:str = "nominal"):
        pruned_ev = self.pruned_ev
        corr = self.corr
        muons = pruned_ev.Muon
        m, n = ak.flatten(muons), ak.num(muons)
        objects_pt_mask = m.pt > 26.01
        objects_eta_mask = np.abs(m.eta) < 2.39
        objects_mask = objects_pt_mask & objects_eta_mask
        in_limit_objects = m.mask[objects_mask]
        objects_pt = ak.fill_none(in_limit_objects.pt, 26.01)
        objects_eta = ak.fill_none(np.abs(in_limit_objects.eta), 0.)
        sf = corr.evaluate(objects_eta, objects_pt, syst)
        sf = ak.where(objects_mask, sf, ak.ones_like(sf))
        sf = ak.unflatten(sf, n)
        sf = ak.prod(sf, axis=1)
        weights_container = Weights(size=len(pruned_ev), storeIndividual=True)
        weights_container.add("sf", sf)
        region_weights = weights_container.weight()
        return region_weights




        