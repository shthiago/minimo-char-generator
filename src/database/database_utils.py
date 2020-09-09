'''Centralize utility functions to access database'''
import json
import sys
from typing import List

from records import Database
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.database.models import Base
from src.database.models import (NameInput, ItemInput,
                                 LoadedDbItemsJson, FeatureInput)


def get_db() -> Database:
    '''Return database object for queries'''
    if settings.TESTING:
        if settings.TEST_DB_URL is None:  # pragma: no cover
            logger.critical('Test database not set')
            sys.exit(1)

        database = Database(settings.TEST_DB_URL)
    else:  # pragma: no cover
        database = Database(settings.DB_URL)

    return database


def init_database(db_url: str) -> None:
    '''Run alembic commands to make migrations to database'''

    engine = create_engine(db_url)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def __load_items(json_data: dict, theme_names: List[str]) -> List[ItemInput]:
    '''Load items from json'''
    items: List[ItemInput] = []
    if 'items' not in json_data \
            and not isinstance(json_data['items'], list):  # pragma: no cover
        return items

    for item in json_data['items']:
        try:
            themes = []
            for theme in item['themes']:
                if theme not in theme_names:  # pragma: no cover
                    logger.error(f'Theme not registered: {theme}')
                    raise KeyError(theme + ' theme')

                themes.append(theme)

            item_input = ItemInput(
                name=item['name'],
                description=item.get('description', ''),
                themes=themes
            )
            items.append(item_input)

        except KeyError as exp:  # pragma: no cover
            logger.error(f'Aborting load of {item}, missing {exp}')

    return items


def __load_names(json_data: dict, theme_names: List[str]) -> List[NameInput]:
    '''Load names from json'''
    names: List[NameInput] = []
    if 'names' not in json_data \
            or not isinstance(json_data['names'], list):  # pragma: no cover
        return names

    for name in json_data['names']:
        try:
            themes = []
            for theme in name['themes']:
                if theme not in theme_names:  # pragma: no cover
                    logger.error(f'Theme not registered: {theme}')
                    raise KeyError(theme + ' theme')

                themes.append(theme)

            name_input = NameInput(
                firstname=name['firstname'],
                lastname=name['lastname'],
                gender=name['gender'].lower(),
                themes=themes
            )

            if name_input.gender not in \
                    settings.CHARACTER_GENDER_POSSIBILITIES:  # pragma: no cover
                raise KeyError('gender not in ' +
                               str(settings.CHARACTER_GENDER_POSSIBILITIES) +
                               ':' + name_input.gender)

            names.append(name_input)

        except KeyError as exp:  # pragma: no cover
            logger.error(f'Aborting load of {name}, missing {exp}')

    return names


def __load_features(json_data: dict,
                    theme_names: List[str]) -> List[FeatureInput]:
    '''Load names from json'''
    features: List[FeatureInput] = []
    if 'features' not in json_data \
            or not isinstance(json_data['features'], list):  # pragma: no cover
        return features

    for feature in json_data['features']:
        try:
            themes = []
            for theme in feature['themes']:
                if theme not in theme_names:  # pragma: no cover
                    logger.error(f'Theme not registered: {theme}')
                    raise KeyError(theme + ' theme')

                themes.append(theme)

            feat_input = FeatureInput(
                text_masc=feature['text_masc'],
                text_fem=feature['text_fem'],
                description=feature['description'],
                is_good=feature['is_good'],
                themes=themes
            )

            features.append(feat_input)

        except KeyError as exp:  # pragma: no cover
            logger.error(f'Aborting load of {feature}, missing {exp}')

    return features


def load_rows_from_json(filename: str) -> LoadedDbItemsJson:
    '''Load database items from JSON'''
    with open(filename) as file:
        data = json.load(file)

    theme_names = []
    if 'themes' in data and isinstance(data['themes'], list):
        theme_names = data['themes']

    logger.info(f'Loaded `{len(theme_names)}` theme names')

    items = __load_items(data, theme_names)

    logger.info(f'Loaded `{len(items)}` items')

    names = __load_names(data, theme_names)

    logger.info(f'Loaded `{len(names)}` names')

    features = __load_features(data, theme_names)

    logger.info(f'Loaded `{len(features)}` features')

    return LoadedDbItemsJson(
        themes=theme_names,
        items=items,
        names=names,
        features=features
    )
