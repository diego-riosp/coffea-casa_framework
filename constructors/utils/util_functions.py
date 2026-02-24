import numpy as np
import awkward as ak
from coffea.nanoevents.methods import candidate
from pathlib import Path
import importlib.util
import subprocess
import json
import gzip
import yaml
    
def loadJson(json_path: str):
    json_path = Path(json_path)

    if json_path.suffix == ".gz":
        with gzip.open(json_path, "rt") as f:
            return json.load(f)
    else:
        with open(json_path, "r") as f:
            return json.load(f)

def writeJson(json_path: str, dictionary):
    
    with open(json_path, "w") as f:
        json.dump(dictionary, f, indent=4)
        
def goldenJson(events, year, lumi_info):
    path = "/home/cms-jovyan/coffea-casa_framework/constructors/selections/sets/"
    goldenjsons = {
        "2022": path + "Cert_Collisions2022_355100_362760_Golden.txt",
    }
    goldenjson = goldenjsons[year]
    is_mc = hasattr(events, "genWeight") and events.genWeight is not None
    if is_mc:
        lumi_mask = np.ones(len(events), dtype="bool")
    else:
        #lumi_info = LumiMask(goldenjson)
        lumi_mask = lumi_info(events.run, events.luminosityBlock)
    return lumi_mask == 1

def loadYaml(yaml_path: str):
    with open(yaml_path) as f:
        yaml_file = yaml.safe_load(f)
    return yaml_file
    
def lorentz_objects(objects):
    return ak.zip(
        {
            "pt": objects.pt,
            "eta": objects.eta,
            "phi": objects.phi,
            "mass": objects.mass,
            "charge": objects.charge,
        },
        with_name="PtEtaPhiMCandidate",
        behavior=candidate.behavior,
    )
    
def dileptons(objects):
    lz_objects = lorentz_objects(objects)
    dileptons = ak.combinations(lz_objects, 2, fields=["l1", "l2"])
    dileptons = dileptons[ak.argsort(dileptons.l1.pt, axis=1)]
    dileptons["p4"] = dileptons.l1 + dileptons.l2
    dileptons["pt"] = dileptons.p4.pt
    return dileptons

def trigger_match_mask(events, leptons):
    trigobjs = events.TrigObj
    pass_pt = trigobjs.pt > 23
    pass_id = abs(trigobjs.id) == 13
    pass_filterbit = trigobjs.filterBits & (0x1 << 3) > 0
    trigger_cands = trigobjs[pass_pt & pass_id & pass_filterbit]
    delta_r = leptons.metric_table(trigger_cands)
    pass_delta_r = delta_r < 0.1
    n_of_trigger_matches = ak.sum(pass_delta_r, axis=2)
    trigger_match_mask = n_of_trigger_matches >= 1
    return ak.sum(trigger_match_mask, axis=-1) > 0

class UtilFunctions:
    
    @classmethod
    def get_active_proxy(cls):
        """
        Returns the active VOMS proxy VO (e.g., 'cms'), or None if no proxy exists.
        """
        try:
            result = subprocess.run(
                ["voms-proxy-info", "--all"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                return None

            for line in result.stdout.splitlines():
                if line.strip().startswith("VO"):
                    return line.split(":")[1].strip()

            return None

        except FileNotFoundError:
            print("ERROR: voms-proxy-info not found in PATH.")
            return None

    @classmethod
    def create_proxy(cls, vo: str = "cms"):
        """
        Creates a silent VOMS proxy using the specified VO.
        """
        print(f"No active proxy found. Creating a new '{vo}' proxy...")
        subprocess.run(
            ["voms-proxy-init", "--voms", vo, "--vomses", "/etc/vomses"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Proxy created.")

    @classmethod
    def main(cls):
        """
        Checks for a VOMS proxy. If none exists, creates a CMS proxy.
        """
        vo = cls.get_active_proxy()

        if vo:
            print(f"Active proxy: {vo}")
        else:
            cls.create_proxy("cms")

if __name__ == "__main__":
    UtilFunctions.main()