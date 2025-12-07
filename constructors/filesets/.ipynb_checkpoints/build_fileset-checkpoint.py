import gzip
import json
import glob
import os
from coffea.dataset_tools.dataset_query import DataDiscoveryCLI
import subprocess
from loadmodule import loadModule
UtilFunctions = loadModule("constructors/utils/util_functions.py")
uf = UtilFunctions()

class BuildFileset:
    def __init__(self):
        return uf.main() #Check or initialize --voms cms
    @staticmethod
    def buildFileset(rucio_query: dict, query_name, scheduler_url: str = "tls://localhost:8786"):
        
        ddc = DataDiscoveryCLI()
        
        ddc.load_dataset_definition(
            rucio_query,
            query_results_strategy="all",
            replicas_strategy="round-robin"
        )
        
        ddc.do_preprocess(
            output_file=f"constructors/filesets/{query_name}_fileset",
            step_size=10000,
            align_to_clusters=False,
            scheduler_url=scheduler_url,
            recalculate_steps="n",
            files_per_batch=1,
            save_form="n",
        )
        
        with gzip.open(f"constructors/filesets/{query_name}_fileset_available.json.gz", "rt") as f:
            fileset_available = json.load(f)
        
        def rucio_to_coffea_fileset(fileset_available, rucio_query):
            fileset = {}
            for pattern, info in rucio_query.items():
                short_name = info["short_name"]
                meta = info.get("meta", {})
                if short_name not in fileset:
                    fileset[short_name] = {"files": {}, "metadata": meta}
                for dataset_name, content in fileset_available.items():
                    if pattern.split("*")[0] in dataset_name:
                        for url, finfo in content["files"].items():
                            fileset[short_name]["files"][url] = finfo.get("object_path", "Events")
        
            return fileset
        fileset = rucio_to_coffea_fileset(fileset_available, rucio_query)
        uf.writeJson(f"constructors/filesets/{query_name}_fileset.json", fileset)
        for gz in glob.glob(f"constructors/filesets/{query_name}*.gz"):
            os.remove(gz)
        return fileset
