from pathlib import Path
import importlib.util
import subprocess
import json
import gzip

class UtilFunctions:

    @staticmethod
    def loadProcessor(processor_name: str):
        """
        Dynamically load a processor class from constructors/processors.
        """
        abs_path = Path.cwd()
        processor_path = abs_path / "constructors" / "processors" / f"{processor_name}.py"

        spec = importlib.util.spec_from_file_location(processor_name, processor_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        class_name = "".join(part.capitalize() for part in processor_name.split("_"))
        return getattr(mod, class_name)

    @staticmethod
    def loadJson(json_path: str):
        """
        Loads a JSON file, supporting both plain .json and .json.gz.
        """
        json_path = Path(json_path)

        if json_path.suffix == ".gz":
            with gzip.open(json_path, "rt") as f:
                return json.load(f)
        else:
            with open(json_path, "r") as f:
                return json.load(f)

    @staticmethod
    def writeJson(json_path: str, dictionary):
        """
        Writes a dictionary to a .json file
        """
        with open(json_path, "w") as f:
            json.dump(dictionary, f, indent=4)

    # ============================================================
    # CLASS METHODS → métodos que operan dentro del contexto de la clase
    # ============================================================

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