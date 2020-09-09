'''DAO for names'''

from typing import Any, Optional, Tuple, List, Dict
from dataclasses import dataclass

from records import Database

from src.database.database_utils import get_db
from src.database.dao.exceptions import InvalidGender
from src.database.dao.dao_utils import SQL_THEME_FILTER_CONDITION
from src.config import settings


@dataclass
class RandNameSelectionSetup:
    '''Class to setup random features selection

    Attributes:
        gender: 'masculine', 'feminine' or 'any'
        filter_themes: optional list of theme names
    '''
    gender: str
    filter_themes: Optional[Tuple[str, ...]] = None


class NameDAO:
    '''Class to manipulate names in database'''

    def __init__(self):
        self.__db: Database = get_db()

    def list_all(self) -> Any:
        '''Return a list with all names'''
        sql = 'SELECT * FROM name'

        return self.__db.query(sql).as_dict()

    def get_random_name(self, setup: RandNameSelectionSetup
                        ) -> Optional[Dict]:
        '''Get random names, optionally filtered by themes'''

        # Data validation
        if setup.gender not in \
                settings.CHARACTER_GENDER_POSSIBILITIES + ['any']:
            raise InvalidGender(setup.gender)

        filter_theme_sql_condition = ''
        if setup.filter_themes:
            filter_theme_sql_condition = SQL_THEME_FILTER_CONDITION

        filter_gender_sql_condition = ''
        if setup.gender != 'any':
            filter_gender_sql_condition = 'AND n.gender=:gender'

        sql = f'''
            SELECT n.* FROM name n, linknametheme lnt, theme t
            WHERE n.id=lnt.id_name AND t.id=lnt.id_theme
            {filter_theme_sql_condition}
            {filter_gender_sql_condition}
            ORDER BY random()
            LIMIT 1
        '''

        result = self.__db.query(sql, gender=setup.gender,
                                 filter_themes=setup.filter_themes)

        ret: List[Dict] = result.as_dict()

        if len(ret) == 0:
            return None

        return ret[0]
