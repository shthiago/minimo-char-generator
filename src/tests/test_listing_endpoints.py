'''Tests for listing endpoints, evaluating the GET requests'''

from fastapi.testclient import TestClient

from src.database.models import LoadedDbItemsJson


def test_names(test_client: TestClient, mock_data: LoadedDbItemsJson) -> None:
    '''Test if names endpoint is returning all registered data'''
    ret = test_client.get('/v1/listing/names').json()

    full_names_ret = [r['firstname'] + r['lastname'] + r['gender']
                      for r in ret]

    full_names_mock = [n.firstname + n.lastname + n.gender
                       for n in mock_data.names]

    assert set(full_names_ret) - set(full_names_mock) == set()  # nosec


def test_features(test_client: TestClient, mock_data: LoadedDbItemsJson) -> None:
    '''Test if features endpoint is returning all registered data'''
    ret = test_client.get('/v1/listing/features').json()

    full_features_ret = [r['text_masc'] + r['text_fem'] +
                         r['description'] + str(r['is_good'])
                         for r in ret]

    full_features_mock = [f.text_masc + f.text_fem +
                          f.description + str(f.is_good)
                          for f in mock_data.features]

    assert set(full_features_ret) - set(full_features_mock) == set()  # nosec


def test_items(test_client: TestClient, mock_data: LoadedDbItemsJson) -> None:
    '''Test if items endpoint is returning all registered data'''
    ret = test_client.get('/v1/listing/items').json()

    full_items_ret = [r['name'] + r['description'] for r in ret]

    full_items_mock = [i.name + i.description for i in mock_data.items]

    assert set(full_items_ret) - set(full_items_mock) == set()  # nosec


def test_themes(test_client: TestClient, mock_data: LoadedDbItemsJson) -> None:
    '''Test if themes endpoint is returning all registered data'''
    ret = test_client.get('/v1/listing/themes').json()

    full_themes_ret = [r['name'] for r in ret]

    assert set(full_themes_ret) - set(mock_data.themes) == set()  # nosec


def test_empty_call(test_client: TestClient) -> None:
    '''Make calls to endpoint, covering all lines of code'''
    ret = test_client.post('/v1/generate', json={})

    assert ret.status_code == 200  # nosec


def test_set_only_gender(test_client: TestClient) -> None:
    '''Test gender filter'''
    ret = test_client.post('/v1/generate', json={'gender': 'masculine'})

    assert ret.status_code == 200  # nosec

    json_ret = ret.json()

    assert json_ret['name']['gender'] == 'masculine'  # nosec

    ret = test_client.post('/v1/generate', json={'gender': 'feminine'})

    assert ret.status_code == 200  # nosec

    json_ret = ret.json()

    assert json_ret['name']['gender'] == 'feminine'  # nosec


def test_set_features(test_client: TestClient) -> None:
    '''Test features set'''
    ret = test_client.post(
        '/v1/generate', json={'n_positive_features': 1, 'n_negative_features': 1})

    assert ret.status_code == 200  # nosec

    ret_json = ret.json()

    assert len(ret_json['positive_features']) == 1  # nosec
    assert len(ret_json['negative_features']) == 1  # nosec
