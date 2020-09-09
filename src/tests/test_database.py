'''Testings for database shape'''
# Disable no-self-use for nice test grouping
# pylint: disable=no-self-use
from records import Database

from src.database.models import LoadedDbItemsJson


def test_db_tables(database):
    '''Validate correct tables in database'''
    tables = database.get_table_names()

    assert 'theme' in tables  # nosec
    assert 'name' in tables  # nosec
    assert 'item' in tables  # nosec
    assert 'feature' in tables  # nosec

    assert 'linknametheme' in tables  # nosec
    assert 'linkitemtheme' in tables  # nosec
    assert 'linkitemtheme' in tables  # nosec


class TestDbPopulation:
    '''Test if popupating functions are working properly'''

    def test_db_populate_names(self, database: Database,
                               mock_data: LoadedDbItemsJson) -> None:
        '''Test populating themes'''
        names_from_db = database.query('SELECT * FROM name').as_dict()

        assert len(names_from_db) == len(mock_data.names)  # nosec

        mock_full_names = [f'{n.firstname} {n.lastname}'
                           for n in mock_data.names]

        db_full_names = [f'{n["firstname"]} {n["lastname"]}'
                         for n in names_from_db]

        assert set(mock_full_names) - set(db_full_names) == set()  # nosec

    def test_db_populate_themes(self, database: Database,
                                mock_data: LoadedDbItemsJson) -> None:
        '''Test populating themes'''
        themes = database.query('SELECT * FROM theme').as_dict()

        assert len(themes) == len(mock_data.themes)  # nosec

        db_themes = [t['name'] for t in themes]

        assert set(mock_data.themes) - set(db_themes) == set()  # nosec

    def test_db_populate_items(self, database: Database,
                               mock_data: LoadedDbItemsJson) -> None:
        '''Test populating items'''
        items = database.query('SELECT * FROM item').as_dict()

        assert len(items) == len(mock_data.items)  # nosec

        db_items = [i['name'] for i in items]
        mock_items = [i.name for i in mock_data.items]

        assert set(mock_items) - set(db_items) == set()  # nosec

    def test_db_populate_link_theme_names(self, database: Database,
                                          mock_data: LoadedDbItemsJson) -> None:
        '''Test links between names and themes'''
        sql = '''
            SELECT theme.name
            FROM name, linknametheme, theme
            WHERE name.id=linknametheme.id_name
                AND theme.id=linknametheme.id_theme
                AND name.firstname=:fname
                AND name.lastname=:lname
        '''

        for name in mock_data.names:
            links = database.query(sql,
                                   fname=name.firstname,
                                   lname=name.lastname).as_dict()
            link_themes = [l['name'] for l in links]

            assert set(link_themes) - set(name.themes) == set()  # nosec

    def test_db_populate_link_theme_items(self, database: Database,
                                          mock_data: LoadedDbItemsJson) -> None:
        '''Test links between names and themes'''
        sql = '''
            SELECT theme.name
            FROM item, linkitemtheme, theme
            WHERE item.id=linkitemtheme.id_item
                AND theme.id=linkitemtheme.id_theme
                AND item.name=:iname
        '''

        for item in mock_data.items:
            links = database.query(sql,
                                   iname=item.name).as_dict()
            link_themes = [l['name'] for l in links]

            assert set(link_themes) - set(item.themes) == set()  # nosec

    def test_db_populate_link_theme_features(self, database: Database,
                                             mock_data: LoadedDbItemsJson) -> None:
        '''Test links between names and themes'''
        sql = '''
            SELECT theme.name
            FROM feature, linkfeaturetheme, theme
            WHERE feature.id=linkfeaturetheme.id_feature
                AND theme.id=linkfeaturetheme.id_theme
                AND feature.text_masc=:tmasc
                AND feature.text_fem=:tfem
        '''

        for feat in mock_data.features:
            links = database.query(sql,
                                   tmasc=feat.text_masc,
                                   tfem=feat.text_fem).as_dict()
            link_themes = [l['name'] for l in links]

            assert set(link_themes) - set(feat.themes) == set()  # nosec
