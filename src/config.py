'''Creation of the base settings object'''
import os
from typing import List


class Settings:
    '''Class to hold settings for application'''
    DB_URL: str = os.environ['DB_URL']

    TEST_DB_URL: str = os.environ.get('TEST_DB_URL', None)

    TESTING: bool = False

    PROJECT_NAME: str = 'Minimum Character Generator'

    BACKEND_CORS_ORIGINS: List[str] = ['*']

    API_V1_STR = '/v1'


settings = Settings()
