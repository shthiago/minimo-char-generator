'''Test the generation tools'''
import pytest

from src.database.dao import FeatureDAO, ItemDAO, NameDAO
from src.database.dao import (RandFeatSelectionSetup,
                              RandItemSelectionSetup,
                              RandNameSelectionSetup)
from src.database.dao.exceptions import (NegativeSelecionTentative,
                                         InvalidGender)
from src.database.models import LoadedDbItemsJson


def test_random_feature_common_use(mock_data: LoadedDbItemsJson):
    '''Validate get random positive and negative features with filter'''
    dao = FeatureDAO()

    setup = RandFeatSelectionSetup(n_features=2,
                                   is_good=True,
                                   filter_themes=('Brasil',))

    feature_names_from_theme = [i.text_masc for i in mock_data.features
                                if 'Brasil' in i.themes]

    features = dao.get_random_features(setup)

    assert len(features) == 2  # nosec
    for feature in features:
        assert feature['is_good']  # nosec
        assert feature['text_masc'] in feature_names_from_theme  # nosec

    setup = RandFeatSelectionSetup(n_features=3,
                                   is_good=False,
                                   filter_themes=('Generico',))

    feature_names_from_theme = [i.text_masc for i in mock_data.features
                                if 'Generico' in i.themes]

    features = dao.get_random_features(setup)

    assert len(features) == 3  # nosec
    for feature in features:
        assert not feature['is_good']  # nosec
        assert feature['text_masc'] in feature_names_from_theme  # nosec


def test_random_feature_unusual_uses():
    '''Test unusual inputs as empty parameters'''
    dao = FeatureDAO()

    setup = RandFeatSelectionSetup(n_features=2,
                                   is_good=True,
                                   filter_themes=('',))

    features = dao.get_random_features(setup)

    assert len(features) == 0  # nosec


def test_negative_feature_numbers():
    '''Pass negative value for number of features'''

    dao = FeatureDAO()

    setup = RandFeatSelectionSetup(n_features=-1, is_good=False)

    with pytest.raises(NegativeSelecionTentative):
        dao.get_random_features(setup)


def test_feature_invalid_theme():
    '''Pass unexistent theme to setup, shall return no results'''
    dao = FeatureDAO()

    setup = RandFeatSelectionSetup(n_features=1,
                                   is_good=False,
                                   filter_themes=('Shenanigan-like-theme',))

    features = dao.get_random_features(setup)

    assert len(features) == 0  # nosec


def test_random_items_common_use(mock_data: LoadedDbItemsJson):
    '''Getting unfiltered and filtered items, with different number'''
    dao = ItemDAO()
    setup = RandItemSelectionSetup(n_items=3)
    items = dao.get_random_items(setup)

    assert len(items) == 3  # nosec

    setup = RandItemSelectionSetup(n_items=5,
                                   filter_themes=('Generico', 'GOT'))
    items = dao.get_random_items(setup)

    item_names_from_themes = [i.name for i in mock_data.items
                              if 'Generico' in i.themes or 'GOT' in i.themes]
    assert len(items) == 5  # nosec
    for item in items:
        assert item['name'] in item_names_from_themes  # nosec


def test_item_invalid_theme():
    '''Pass unexistant theme to filter'''
    dao = ItemDAO()
    setup = RandItemSelectionSetup(n_items=1,
                                   filter_themes=('PizzaFritaNaLareira',))
    items = dao.get_random_items(setup)

    assert len(items) == 0  # nosec


def test_item_zero():
    '''Pass unexistant theme to filter'''
    dao = ItemDAO()
    setup = RandItemSelectionSetup(n_items=0)
    items = dao.get_random_items(setup)

    assert len(items) == 0  # nosec


def test_item_negative():
    '''Try to get a negative number of items'''
    dao = ItemDAO()
    setup = RandItemSelectionSetup(n_items=-1)
    with pytest.raises(NegativeSelecionTentative):
        dao.get_random_items(setup)


def test_random_name_common_use(mock_data: LoadedDbItemsJson):
    '''Test filtered and unfiltered names selection'''

    dao = NameDAO()

    setup = RandNameSelectionSetup(gender='masculine')
    masc_name = dao.get_random_name(setup)
    assert masc_name  # nosec

    setup = RandNameSelectionSetup(gender='feminine')
    fem_name = dao.get_random_name(setup)
    assert fem_name  # nosec

    setup = RandNameSelectionSetup(gender='neutral')
    nutral_name = dao.get_random_name(setup)
    assert nutral_name  # nosec

    setup = RandNameSelectionSetup(gender='any')
    any_gender = dao.get_random_name(setup)
    assert any_gender  # nosec

    setup = RandNameSelectionSetup(gender='masculine',
                                   filter_themes=('Brasil',))
    name = dao.get_random_name(setup)
    names_from_theme = [i.firstname+i.lastname for i in mock_data.names
                        if 'Brasil' in i.themes]

    assert isinstance(name, dict)  # nosec
    assert name['firstname'] + name['lastname'] in names_from_theme  # nosec

    setup = RandNameSelectionSetup(gender='masculine',
                                   filter_themes=('Brasil', 'GOT'))
    name = dao.get_random_name(setup)
    names_from_theme = [i.firstname+i.lastname for i in mock_data.names
                        if 'Brasil' in i.themes or 'GOT' in i.themes]

    assert isinstance(name, dict)  # nosec
    assert name['firstname'] + name['lastname'] in names_from_theme  # nosec


def test_random_name_invalid_gender():
    '''Try to select a nem with a invalid gender'''
    dao = NameDAO()
    setup = RandNameSelectionSetup(gender='pizzaiolo')

    with pytest.raises(InvalidGender):
        dao.get_random_name(setup)


def test_random_name_invalid_theme():
    '''Try to get a name with invalid theme'''
    dao = NameDAO()
    setup = RandNameSelectionSetup(gender='masculine',
                                   filter_themes=('Pizzaria',))

    name = dao.get_random_name(setup)

    assert name is None  # nosec
