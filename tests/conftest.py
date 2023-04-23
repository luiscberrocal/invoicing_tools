import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pytest
from dotenv import load_dotenv

from invoicing_tools.config.configuration import ConfigurationManager
from invoicing_tools.db.managers import JSONDatabase


@pytest.fixture(scope='session')
def output_folder():
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def fixtures_folder():
    folder = Path(__file__).parent.parent / 'tests' / 'fixtures'
    return folder


@pytest.fixture(scope='session')
def envs_folder() -> Path:
    folder = Path(__file__).parent.parent / '.envs'
    return folder


@pytest.fixture(scope='session')
def google_secrets_file(envs_folder) -> Path:
    g_file = envs_folder / 'client_secret.json'
    return g_file


@pytest.fixture(scope='session')
def app_configuration(envs_folder) -> Dict[str, Any]:
    g_file = envs_folder / 'app_configuration.json'
    with open(g_file, 'r') as j_file:
        config = json.load(j_file)
    return config


@pytest.fixture(scope='session')
def raw_file_list(envs_folder) -> List[Dict[str, Any]]:
    g_file = envs_folder / 'raw_files.json'
    with open(g_file, 'r') as j_file:
        data = json.load(j_file)
    return data


@pytest.fixture(scope='session')
def database(envs_folder) -> JSONDatabase:
    g_file = envs_folder / 'json_db2.json'
    db = JSONDatabase(g_file)
    return db


@pytest.fixture(scope='session')
def app_config(envs_folder) -> Dict[str, Any]:
    configuration_manager = ConfigurationManager(envs_folder / ConfigurationManager.DEFAULT_CONFIG_FOLDER_NAME)
    # sample = configuration_manager.get_sample_config()
    # configuration_manager.write_configuration(sample,overwrite=True)
    return configuration_manager.get_configuration()

@pytest.fixture()
def load_environment_variables(envs_folder) -> None:
    file = envs_folder / 'env.txt'
    load_dotenv(file)
