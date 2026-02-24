from loadmodule import loadFunction

apply_muon_smearing_corrections_run3 = loadFunction("constructors/corrections/objects/muons.py", "apply_muon_smearing_corrections_run3")

class ObjectCorrector:
    def __init__(self, events):
        self.events = events

    def muonSmearing(self, smearing):
        events = self.events
        apply_muon_smearing_corrections_run3(events, smearing)