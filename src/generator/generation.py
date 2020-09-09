'''Character generting functions'''

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple

from loguru import logger

from src.generator.exceptions import NoDataForGeneration
from src.database.dao import FeatureDAO, NameDAO, ItemDAO
from src.database.dao import (RandFeatSelectionSetup,
                              RandItemSelectionSetup,
                              RandNameSelectionSetup)


@dataclass
class GenerationSetup:
    '''A model for name input, in populating names

    Attributes:
        themes: optional theme string
        gender: optional character gender

        items: number of items, default 3
        n_positive_features: number of positive features, default 5
        n_negative_features: number of negative features, default 3
    '''
    gender: str
    items: int
    n_positive_features: int
    n_negative_features: int
    themes: Optional[Tuple[str, ...]] = None


def treat_no_data_for_generation(log: str) -> None:
    '''Log input and  raise exception'''
    logger.warning(log)
    raise NoDataForGeneration(log)


def get_positive_features(n_features: int,
                          themes: Optional[Tuple[str, ...]]) -> List[Dict]:
    '''Select random positive features'''
    dao = FeatureDAO()

    setup = RandFeatSelectionSetup(
        n_features=n_features,
        is_good=True,
        filter_themes=themes)

    positive_features = dao.get_random_features(setup)

    log = None
    if not positive_features:
        log = f'No positive features for themes `{themes}`'

    elif len(positive_features) < n_features:
        log = f'Not enough positive feats for themes `{themes}``.' + \
            f'Expected `{n_features}`, found ' + \
            f'`{len(positive_features)}`'
    if log:
        treat_no_data_for_generation(log)

    return positive_features


def get_negative_features(n_features: int,
                          themes: Optional[Tuple[str, ...]]) -> List[Dict]:
    '''Select random negative features'''
    dao = FeatureDAO()

    setup = RandFeatSelectionSetup(
        n_features=n_features,
        is_good=False,
        filter_themes=themes)

    negative_features = dao.get_random_features(setup)

    log = None
    if not negative_features:
        log = f'No negative features for themes `{themes}`'

    elif len(negative_features) < n_features:
        log = f'Not enough negative feats for themes `{themes}``.' + \
              f'Expected `{n_features}`, found ' + \
              f'`{len(negative_features)}`'

    if log:
        treat_no_data_for_generation(log)

    return negative_features


def get_name(gender: str, themes: Optional[Tuple[str, ...]] = None) -> Optional[Dict]:
    '''Select a random name'''
    dao = NameDAO()
    setup = RandNameSelectionSetup(gender=gender, filter_themes=themes)

    name = dao.get_random_name(setup)

    if not name:
        treat_no_data_for_generation(
            f'No name with gender `{gender}` and themes `{themes}`')

    return name


def get_items(n_items: int, themes: Optional[Tuple[str, ...]] = None) -> List[Dict]:
    '''Select random items'''
    dao = ItemDAO()
    setup = RandItemSelectionSetup(n_items=n_items, filter_themes=themes)

    items = dao.get_random_items(setup)

    log = None
    if not items:
        log = f'No items for themes `{themes}`'

    elif len(items) < n_items:
        log = f'Not enough items for themes `{themes}`. ' + \
              f'Expected {n_items}, found {len(items)}'

    if log:
        treat_no_data_for_generation(log)

    return items


def generate_character(setup: GenerationSetup) -> Dict:
    '''Run the generation parametrized'''
    name = get_name(gender=setup.gender, themes=setup.themes)

    positive_features = get_positive_features(
        n_features=setup.n_positive_features,
        themes=setup.themes)

    negative_features = get_negative_features(
        n_features=setup.n_negative_features,
        themes=setup.themes)

    items = get_items(n_items=setup.items, themes=setup.themes)

    return {
        'name': name,
        'positive_features': positive_features,
        'negative_features': negative_features,
        'items': items
    }
