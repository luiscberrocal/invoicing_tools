import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture(scope='session')
def output_folder():
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def fixtures_folder():
    folder = Path(__file__).parent.parent / 'tests' / 'fixtures'
    return folder


@pytest.fixture(scope='session')
def envs_folder():
    folder = Path(__file__).parent.parent / '.envs'
    return folder


@pytest.fixture(scope='session')
def google_secrets_file(envs_folder):
    g_file = envs_folder / 'client_secret.json'
    return g_file


@pytest.fixture(scope='session')
def app_configuration(envs_folder) -> Dict[str, Any]:
    g_file = envs_folder / 'app_configuration.json'
    with open(g_file, 'r') as j_file:
        config = json.load(j_file)
    return config
