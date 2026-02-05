import copy
import hist
import awkward as ak
from coffea import processor
from loadmodule import loadModule
from coffea.lumi_tools import LumiMask


#Dinamically load modules
LoadCorrectionSet = loadModule("constructors/corrections/load_correction_set.py")
ObjectCorrector = loadModule("constructors/corrections/object_corrector.py")
ObjectSelector = loadModule("constructors/selections/object_selector.py")
EventSelector = loadModule("constructors/selections/event_selector.py")
EventCorrector = loadModule("constructors/corrections/event_corrector.py")
HistogramFiller = loadModule("constructors/histograms/histogram_filler.py")

class MuonProcessor(processor.ProcessorABC):
    def __init__(self, year, corr_dict):
        self.year = year
        corr_loader = LoadCorrectionSet(year, corr_dict)
        for attr in dir(corr_loader):
            if attr.endswith("corr"):
                setattr(self, attr, getattr(corr_loader, attr))
        
        self._hist_template = hist.Hist.new.Reg(
            30, 60, 120, 
            name="mass", 
            label="mμμ [GeV]"
        ).Weight()

        self.lumi_info = LumiMask("constructors/selections/sets/Cert_Collisions2022_355100_362760_Golden.txt")

    def process(self, events):
        dataset = events.metadata["dataset"]
        
        h_mass = self._hist_template.copy()

        ObjectCorrector(events).muonSmearing(self.smearing_objcorr)
        muons, dimuons, mass = ObjectSelector(events).muonSelector()
        pruned_ev, pruned_mass = EventSelector(events, self.year, self.lumi_info).selectEvents(muons, dimuons, mass)
        region_weights = EventCorrector(
            pruned_ev, 
            self.muon_Z_id_evcorr, 
            self.muon_Z_iso_evcorr, 
            self.muon_Z_trg_evcorr
        ).scaleFactors("nominal")

        xsecs = {'DYJetsToLL': 6688, 'DYJetsToLL_HT': 911.4, 'TTbar': 97.78, 'SingleTop': 4.66, 'Diboson': 122.3}
        is_mc = "genWeight" in events.fields
        xsec = xsecs.get(dataset, 1.0) if is_mc else None
        HistogramFiller(events, h_mass).fillHistogram(region_weights, pruned_ev, pruned_mass, xsec)
        
        return {
            dataset: {
                "mass": h_mass,
                "nevents": len(pruned_ev)
            }
        }

    def postprocess(self, accumulator):
        return accumulator