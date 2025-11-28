import awkward as ak
import numpy as np
import correctionlib
import hist
from coffea import processor
#from pathlib import Path
#import importlib
#from constructors.corrections import CorrectionsLoader

class MuonProcessor(processor.ProcessorABC):
    def __init__(self, sf_path: str):
        self.corrections = correctionlib.CorrectionSet.from_file(sf_path)
        self.muon_sf = self.corrections["NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight"]

    def process(self, events):
        dataset = events.metadata["dataset"]
        h_mass = hist.Hist.new.StrCat([], growth=True, name="dataset").Reg(
            60, 60, 120, name="mass", label="mμμ test [GeV]"
        ).Weight()

        muons = events.Muon[events.Muon.tightId]
        dimuons = ak.combinations(muons, 2, fields=["lead", "trail"])
        
        dimuons = dimuons[(dimuons.lead.charge != dimuons.trail.charge)]
        
        def ak_clip(x, lo, hi):
            return ak.where(x > hi, hi, ak.where(x < lo, lo, x))
        
        eta_lead, pt_lead = ak_clip(dimuons.lead.eta, -2.39, 2.39), ak_clip(dimuons.lead.pt, 26.01, np.inf)
        eta_trail, pt_trail = ak_clip(dimuons.trail.eta, -2.39, 2.39), ak_clip(dimuons.trail.pt, 26.01, np.inf)
        
        sf_lead  = self.muon_sf.evaluate(eta_lead,  pt_lead,  "nominal")
        sf_trail = self.muon_sf.evaluate(eta_trail, pt_trail, "nominal")

        #CL = CorrectionsLoader(events,self.muon_sf)
        #sf_lead = CL.scaleFactors(dimuons.lead,"nominal")
        #sf_trail = CL.scaleFactors(dimuons.trail,"nominal")
        
        event_weight = sf_lead * sf_trail
        mass = (dimuons.lead + dimuons.trail).mass
        
        mass_flat = ak.to_numpy(ak.flatten(mass))
        weight_flat = ak.to_numpy(ak.flatten(event_weight))
        
        h_mass.fill(
            dataset=dataset,
            mass=mass_flat,
            weight=weight_flat,
        )

        return {
            "entries": ak.num(events, axis=0),
            "mass": h_mass,
        }

    def postprocess(self, accumulator):
        return accumulator