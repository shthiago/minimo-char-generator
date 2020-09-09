'''DAO for features'''

from typing import Any, Optional, List, Dict, Tuple
from dataclasses import dataclass

from records import Database

from src.database.database_utils import get_db
from src.database.dao.exceptions import NegativeSelecionTentative


@dataclass
class RandFeatSelectionSetup:
    '''Class to setup random features selection

    Attributes:
        n_features: number of features to get
        is_good: might the features be positive?
        filter_themes: optional list of theme names
    '''
    n_features: int
    is_good: bool
    filter_themes: Optional[Tuple[str, ...]] = None


class FeatureDAO:
    '''Class to manipulate features in database'''

    def __init__(self):
        self.__db: Database = get_db()

    def list_all(self) -> Any:
        '''Return a list with all features'''
        sql = 'SELECT * FROM feature'

        return self.__db.query(sql).as_dict()

    def get_random_features(self, setup: RandFeatSelectionSetup
                            ) -> List[Dict]:
        '''Get n random features as filtered (is_good and theme)'''

        # Data validation
        if setup.n_features < 0:
            raise NegativeSelecionTentative()

        filter_theme_sql_condition = ''
        if setup.filter_themes:
            filter_theme_sql_condition = '''AND t.id IN (
                SELECT id FROM theme WHERE name IN :theme_names
            )'''

        sql = f'''
            SELECT f.* FROM feature f, linkfeaturetheme lft, theme t
            WHERE f.id=lft.id_feature AND t.id=lft.id_theme
            AND is_good=:is_good
            {filter_theme_sql_condition}
            ORDER BY random()
            LIMIT :n_features
        '''

        result = self.__db.query(sql,
                                 is_good=setup.is_good,
                                 n_features=setup.n_features,
                                 theme_names=setup.filter_themes)

        ret: List[Dict] = result.as_dict()

        return ret
