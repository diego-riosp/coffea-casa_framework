import correctionlib
from coffea import processor
from loadmodule import loadModule, loadFunction

#Dinamically load modules
ObjectSelector = loadModule("constructors/selections/object_selector.py")
EventSelector = loadModule("constructors/selections/event_selector.py")
EventCorrector = loadModule("constructors/corrections/event_corrector.py")
HistogramFiller = loadModule("constructors/histograms/histogram_filler.py")

#Dinamically load functions
#apply_rochester_corrections_run2 = loadFunction("constructors/corrections/crystall_ball.py", "apply_rochester_corrections_run2")

class MuonProcessor(processor.ProcessorABC):
    def __init__(self, cset_file:str, cname:str):
        #met_cset_file = "constructors/corrections/sets/run3_met_xy_corrections.json"
        #self.met_cset = correctionlib.CorrectionSet.from_file(cset_file)
        
        cset = correctionlib.CorrectionSet.from_file(cset_file)
        self.corr = cset[cname]

    def process(self, events):
        
        ##################object correction
        #apply_rochester_corrections_run2(events, self.met_cset, "2018")
        
        ##################object selection
        dimuons, mass = ObjectSelector(events).muonSelector()
        
        ##################event selection
        pruned_ev, pruned_mass = EventSelector(events).selectEvents(dimuons, mass)
        
        ##################event correction
        region_weights = EventCorrector(pruned_ev,self.corr).scaleFactors("nominal")
        ##################fill and normalize histograms
        histograms = HistogramFiller(events).fillHistogram(region_weights,pruned_mass)

        return histograms

    def postprocess(self, accumulator):
        return accumulator