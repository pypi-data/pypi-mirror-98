"""Can run a python module directly from code.
"""
from typing import List, Optional


def load_module(name: str):
    try:
        import importlib

        return importlib.import_module(name)
    except Exception as e:
        raise Exception(f"failed to import module {name}") from e


def run(comp, *, gada_config: dict, node_config: dict, argv: Optional[List] = None):
    # Check the entrypoint is configured
    entrypoint = node_config.get("entrypoint", None)
    if not entrypoint:
        raise Exception("missing entrypoint in configuration")

    # Load module if explicitely configured
    if "module" in node_config:
        comp = load_module(node_config["module"])

    # Check the entrypoint exists
    fun = getattr(comp, entrypoint, None)
    if not fun:
        raise Exception(f"module {comp.__name__} has no entrypoint {entrypoint}")

    # Call entrypoint
    fun(argv=argv)
