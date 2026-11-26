import importlib.util
from pathlib import Path


def test_analytical_round_trip():
    path = Path(__file__).resolve().parents[2] / "services/data-engineering/technical_smoke.py"
    spec = importlib.util.spec_from_file_location("technical_smoke", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.run() == (2, 10, 10)
