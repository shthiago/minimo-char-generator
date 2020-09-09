'''Testing configurations'''
# Disable redefined-outer-name because of fixture chaining
# pylint: disable=redefined-outer-name
import os

import pytest
from fastapi.testclient import TestClient
from records import Database

from src.api import app
from src.database.database_utils import load_rows_from_json
from src.database.models import LoadedDbItemsJson
from src.database.populate import populate_mock
from src.database.database_utils import init_database, get_db
from src.config import settings

settings.TESTING = True


@pytest.fixture(scope='package')
def test_client() -> TestClient:
    '''Create a test client'''
    return TestClient(app)


@pytest.fixture(scope='package')
def mock_data() -> LoadedDbItemsJson:
    '''Load mock data from json'''
    file_dir = os.path.dirname(__file__)
    json_rows = load_rows_from_json(os.path.join(file_dir, 'mock_db.json'))

    return json_rows


@pytest.fixture(scope='package')
def database(mock_data: LoadedDbItemsJson) -> Database:
    '''Initialized database for testing'''
    test_db = get_db()
    init_database(test_db.db_url)

    populate_mock(mock_data, test_db)

    yield test_db

    # teardown
    with test_db.transaction() as conn:
        conn.query('DROP TABLE linkfeaturetheme')
        conn.query('DROP TABLE linknametheme')
        conn.query('DROP TABLE linkitemtheme')

        conn.query('DROP TABLE theme')
        conn.query('DROP TABLE name')
        conn.query('DROP TABLE item')
        conn.query('DROP TABLE feature')
