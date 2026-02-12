import copy
import hist
import awkward as ak
from coffea import processor
from loadmodule import loadAll
from coffea.lumi_tools import LumiMask

constructors = "constructors/"

modules = [
    "corrections/load_correction_set.py",
    "corrections/object_corrector.py",
    "selections/object_selector.py",
    "selections/event_selector.py",
    "corrections/event_corrector.py",
    "histograms/histogram_filler.py",
    "utils/util_functions.py",
]

for mod in modules:
    loadAll(f"{constructors}{mod}")

class MuonProcessor(processor.ProcessorABC):
    def __init__(self, workflow_path, year, corr_dict):
        self.year = year
        corr_loader = LoadCorrectionSet(year, corr_dict)
        for attr in dir(corr_loader):
            if attr.endswith("corr"):
                setattr(self, attr, getattr(corr_loader, attr))
        
        self._histogram = hist.Hist.new.Reg(
            30, 60, 120, 
            name="mass", 
            label="mμμ [GeV]"
        ).Weight()

        self.lumi_info = LumiMask("constructors/selections/sets/Cert_Collisions2022_355100_362760_Golden.txt")
        self.workflow = loadYaml(workflow_path)

    def process(self, events):
        workflow = self.workflow
        dataset = events.metadata["dataset"]
        is_mc = "genWeight" in events.fields
        sumw = ak.sum(events.genWeight) if is_mc else len(events)
        histogram = self._histogram.copy()

        ObjectCorrector(events).muonSmearing(self.smearing_objcorr)
        
        objects = objectSelector(events, workflow)
        pruned_events = eventSelector(events, objects, workflow, self.year, self.lumi_info)
        objects = objectSelector(pruned_events, workflow)
        
        if is_mc:
            region_weights = EventCorrector(
                pruned_events, 
                self.muon_Z_id_evcorr, 
                self.muon_Z_iso_evcorr, 
                self.muon_Z_trg_evcorr
            ).scaleFactors("nominal")
        else:
            region_weights = ak.ones_like(pruned_events.event)
        HistogramFiller(events, histogram, is_mc, sumw).fillHistogram(region_weights, objects)
        
        return {
            dataset: {
                "mass": histogram,
                "nevents": len(pruned_events)
            }
        }

    def postprocess(self, accumulator):
        return accumulator