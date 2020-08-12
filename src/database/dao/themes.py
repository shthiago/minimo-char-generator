'''DAO for themes'''

from typing import List, Dict

from records import Database

from src.database.database_utils import get_db


class ThemeDAO:
    '''Class to manipulate themes in database'''

    def __init__(self):
        self.__db: Database = get_db()

    def list_all(self) -> List[Dict]:
        '''Return a list with all themes'''
        sql = 'SELECT * FROM theme'

        return self.__db.query(sql).as_dict()
