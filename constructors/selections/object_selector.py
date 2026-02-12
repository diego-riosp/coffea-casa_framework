import yaml
from loadmodule import loadAll
loadAll("constructors/utils/util_functions.py")

class SelectionEngine:
    def __init__(self, cfg, context):
        self.cfg = cfg
        self.context = context
        self.objects = {}
        
    def eval_expr(self, expr, local_ctx=None):
        ctx = self.context | {"objects": self.objects}

        if local_ctx:
            ctx |= local_ctx

        try:
            return eval(expr, {}, ctx)
        except Exception as e:
            raise RuntimeError(f"[DSL ERROR] Expression: '{expr}'\n{type(e).__name__}: {e}")

    def normalize_expr(self, expr, obj_name):
        expr = expr.replace(f"{obj_name}.", "obj.")
        return expr

    def apply(self):
        if "object_selection" not in self.cfg:
            raise ValueError("YAML must contain top-level key: 'objects'")

        for name, block in self.cfg["object_selection"].items():

            if "object" not in block:
                raise ValueError(f"Object '{name}' missing 'object' field in YAML")
            if "cuts" not in block:
                raise ValueError(f"Object '{name}' missing 'cuts' field in YAML")

            obj = self.eval_expr(block["object"])

            mask = None
            for raw_cut in block["cuts"]:
                cut = self.normalize_expr(raw_cut, name)
                m = self.eval_expr(cut, {"obj": obj})
                mask = m if mask is None else (mask & m)

            obj = obj[mask]
            self.objects[name] = obj

        return self.objects

def objectSelector(events, workflow):

    engine = SelectionEngine(
        workflow,
        context={
            "events": events,
            "dileptons": dileptons,
            "abs": abs
        }
    )

    objects = engine.apply()
    return objects
