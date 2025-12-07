import importlib.util
from pathlib import Path

def loadModule(module_path: str):
    path = Path(module_path)
    if path.suffix != ".py":
        raise ValueError(f"Module path must end with .py, got: {module_path}")
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"Could not load spec for: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    class_name = "".join(part.capitalize() for part in module_name.split("_"))
    return getattr(mod, class_name)

def loadFunction(module_path: str, function_name: str):
    path = Path(module_path)
    if path.suffix != ".py":
        raise ValueError(f"Module path must end with .py, got: {module_path}")

    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"Could not load spec for: {path}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return getattr(mod, function_name)