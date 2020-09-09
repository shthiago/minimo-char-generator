'''Creation of the base settings object'''
import os
from typing import List, Optional


class Settings:
    '''Class to hold settings for application'''
    DB_URL: Optional[str] = os.environ.get('DB_URL', None)

    TEST_DB_URL: Optional[str] = os.environ.get('TEST_DB_URL', None)

    TESTING: bool = bool(os.environ.get('TEST_MODE', False))

    PROJECT_NAME: str = 'Minimum Character Generator'

    BACKEND_CORS_ORIGINS: List[str] = ['*']

    API_V1_STR = '/v1'

    CHARACTER_GENDER_POSSIBILITIES = ['masculine', 'feminine', 'neutral']


settings = Settings()
