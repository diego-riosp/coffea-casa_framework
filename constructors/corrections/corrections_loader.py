import correctionlib
import awkward as ak

class CorrectionsLoader:
    def __init__(self, events, sf):
        self.events = events
        self.sf = sf
        
    def correctionsExplorer():
        return 0
        
    def scaleFactors(self, objects: str, syst: str = "nominal"):
        events = self.events
        sf = self.sf
        
        def ak_clip(x, lo, hi):
            return ak.where(x > hi, hi, ak.where(x < lo, lo, x))
            
        eta, pt = ak_clip(objects.eta, -2.39, 2.39), ak_clip(objects.pt, 26.01, np.inf)
        
        sf = sf.evaluate(eta, pt, syst)

        sf = ak.prod(sf, axis=1)

        return sf