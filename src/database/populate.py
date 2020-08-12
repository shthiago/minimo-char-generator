'''Functions to insert rows into database'''
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError
from records import Database

from src.database.models import (NameInput, ItemInput,
                                 LoadedDbItemsJson, FeatureInput)


def populate_themes(themes: List[str], database: Database) -> None:
    '''Populate database for testing purposes

    On conflict, do nothing

    Parameters
    ----------
    themes: List[str]
        list of themes names
    database: Database
        db instance
    '''

    sql = '''INSERT INTO theme (name) VALUES (:name)
             ON CONFLICT (name) DO NOTHING;'''

    conn = database.get_connection()
    transaction = conn.transaction()
    try:
        for name in themes:
            conn.query(sql, name=name)
        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()


def populate_names(names: List[NameInput], database: Database) -> None:
    '''Populate names

    On conflict, just do nothing

    Parameters
    ----------
    names: List[NameInput]
        list of structured names
    database: Database
        db instance
    '''
    sql = '''INSERT INTO name (firstname, lastname, gender)
        VALUES (:firstname, :lastname, :gender)
        ON CONFLICT ON CONSTRAINT name_firstname_lastname_key
        DO NOTHING;
    '''

    conn = database.get_connection()
    transaction = conn.transaction()

    try:
        for name in names:
            conn.query(sql,
                       firstname=name.firstname,
                       lastname=name.lastname,
                       gender=name.gender)
        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()

    sql = '''INSERT INTO linknametheme (id_theme, id_name)
        VALUES (
            (SELECT id FROM theme t
                WHERE t.name=:theme_name),
            (SELECT id FROM name n
                WHERE n.firstname=:fname
                AND n.lastname=:lname)
            )
        ON CONFLICT DO NOTHING;
    '''
    conn = database.get_connection()
    transaction = conn.transaction()
    try:
        for name in names:
            for theme in name.themes:
                conn.query(sql,
                           theme_name=theme,
                           fname=name.firstname,
                           lname=name.lastname)

        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()


def populate_items(items: List[ItemInput], database: Database) -> None:
    '''Populate names

    On conflict, just do nothing

    Parameters
    ----------
    items: List[ItemInput]
        list of structured items
    database: Database
        db instance
    '''
    sql = '''INSERT INTO item (name, description)
        VALUES (:name, :description)
        ON CONFLICT (name) DO NOTHING;
    '''

    conn = database.get_connection()
    transaction = conn.transaction()
    try:
        for item in items:
            conn.query(sql,
                       name=item.name,
                       description=item.description)
        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()

    sql = '''INSERT INTO linkitemtheme (id_theme, id_item)
        VALUES (
            (SELECT id FROM theme t
                WHERE t.name=:theme_name),
            (SELECT id FROM item i
                WHERE i.name=:item_name)
            )
        ON CONFLICT DO NOTHING;
    '''
    conn = database.get_connection()
    transaction = conn.transaction()
    try:
        for item in items:
            for theme in item.themes:
                conn.query(sql,
                           theme_name=theme,
                           item_name=item.name)

        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()


def populate_features(features: List[FeatureInput], database: Database) -> None:
    '''Populate names

    On conflict, just do nothing

    Parameters
    ----------
    features: List[FeatureInput]
        list of structured features
    database: Database
        db instance
    '''

    sql = '''INSERT INTO feature (text_masc, text_fem, description, is_good)
        VALUES (:text_masc, :text_fem, :description, :is_good)
        ON CONFLICT DO NOTHING;
    '''

    conn = database.get_connection()
    transaction = conn.transaction()
    try:
        for feature in features:
            conn.query(sql,
                       text_masc=feature.text_masc,
                       text_fem=feature.text_fem,
                       description=feature.description,
                       is_good=feature.is_good)
        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()

    sql = '''INSERT INTO linkfeaturetheme (id_theme, id_feature)
        VALUES (
            (SELECT id FROM theme t
                WHERE t.name=:theme_name),
            (SELECT id FROM feature f
                WHERE f.text_masc=:tmasc
                AND f.text_fem=:tfem)
            )
        ON CONFLICT DO NOTHING;
    '''
    conn = database.get_connection()
    transaction = conn.transaction()
    try:
        for feature in features:
            for theme in feature.themes:
                conn.query(sql,
                           theme_name=theme,
                           tmasc=feature.text_masc,
                           tfem=feature.text_fem)

        transaction.commit()

    except IntegrityError as ierror:
        logger.error(ierror)
        transaction.rollback()
        raise
    finally:
        conn.close()


def populate_mock(data: LoadedDbItemsJson, database: Database) -> None:
    '''Create mock DB for testing purposes'''
    populate_themes(data.themes, database)

    populate_names(data.names, database)

    populate_items(data.items, database)

    populate_features(data.features, database)
