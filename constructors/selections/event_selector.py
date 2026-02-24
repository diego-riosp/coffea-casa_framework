import numpy as np
import awkward as ak
from coffea.analysis_tools import PackedSelection
from loadmodule import loadAll
loadAll("constructors/utils/util_functions.py")

class EventSelectionEngine:
    def __init__(self, cfg, context):
        self.cfg = cfg
        self.context = context
        self.selections = PackedSelection()
        self.masks = {}

    def eval_expr(self, expr):
        try:
            return eval(expr, {}, self.context)
        except Exception as e:
            raise RuntimeError(f"[EVENT DSL ERROR] Expression: '{expr}'\n{type(e).__name__}: {e}")

    def build(self):
        if "event_selection" not in self.cfg:
            raise ValueError("YAML must contain 'event_selection' block")

        for name, expr in self.cfg["event_selection"].items():
            mask = self.eval_expr(expr)
            self.selections.add(name, mask)
            self.masks[name] = mask

        return self.selections

    def apply_region(self, region_name):
        if "regions" not in self.cfg:
            raise ValueError("No 'regions' block in YAML")

        if region_name not in self.cfg["regions"]:
            raise ValueError(f"Region '{region_name}' not defined in YAML")

        cuts = self.cfg["regions"][region_name]
        return self.selections.all(*cuts)

def eventSelector(events, objects, workflow, year, lumi_info):
    event_engine = EventSelectionEngine(
        workflow,
        context={
            "events": events,
            "year": year,
            "lumi_info": lumi_info,
            "objects": objects,
            "goldenJson": goldenJson,
            "trigger_match_mask": trigger_match_mask,
            "ak": ak
        }
    )

    selections = event_engine.build()
    region_mask = event_engine.apply_region("signal_region")

    pruned_events = events[region_mask]

    return pruned_events
