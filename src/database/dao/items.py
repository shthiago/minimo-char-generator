'''DAO for items'''

from typing import Any, Tuple, Optional, Dict, List
from dataclasses import dataclass

from records import Database

from src.database.database_utils import get_db
from src.database.dao.exceptions import NegativeSelecionTentative
from src.database.dao.dao_utils import SQL_THEME_FILTER_CONDITION


@dataclass
class RandItemSelectionSetup:
    '''Class to setup random items selection

    Attributes:
        n_items: number of items to get
        filter_themes: optional list of theme names
    '''
    n_items: int
    filter_themes: Optional[Tuple[str, ...]] = None


class ItemDAO:
    '''Class to manipulate items in database'''

    def __init__(self):
        self.__db: Database = get_db()

    def list_all(self) -> Any:
        '''Return a list with all items'''
        sql = 'SELECT * FROM item'

        return self.__db.query(sql).as_dict()

    def get_random_items(self, setup: RandItemSelectionSetup) -> List[Dict]:
        '''Get random items, optinally filtered by a theme names'''

        # Data validation
        if setup.n_items < 0:
            raise NegativeSelecionTentative()

        filter_theme_sql_condition = ''
        if setup.filter_themes:
            filter_theme_sql_condition = SQL_THEME_FILTER_CONDITION

        sql = f'''
            SELECT i.* FROM item i, linkitemtheme lit, theme t
            WHERE i.id=lit.id_item AND t.id=lit.id_theme
            {filter_theme_sql_condition}
            ORDER BY random()
            LIMIT :n_items
        '''

        result = self.__db.query(sql, n_items=setup.n_items,
                                 filter_themes=setup.filter_themes)

        ret: List[Dict] = result.as_dict()

        return ret
