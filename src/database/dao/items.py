'''DAO for items'''

from typing import List, Dict

from records import Database

from src.database.database_utils import get_db


class ItemDAO:
    '''Class to manipulate features in database'''

    def __init__(self):
        self.__db: Database = get_db()

    def list_all(self) -> List[Dict]:
        '''Return a list with all items'''
        sql = 'SELECT * FROM item'

        return self.__db.query(sql).as_dict()
