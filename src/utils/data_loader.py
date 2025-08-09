import yaml
from pathlib import Path
from src.utils.config_loader import load_config

def load_test_data(env=None):
    cfg = load_config()
    env = env or cfg.get("env", "qa")
    path = Path("data/testdata.yaml")
    with open(path) as f:
        all_data = yaml.safe_load(f)
    return all_data.get(env, {})

# Pytest fixture
import pytest

@pytest.fixture(scope="session")
def test_data():
    cfg = load_config()
    env = cfg.get("env", "qa")
    return load_test_data(env)
