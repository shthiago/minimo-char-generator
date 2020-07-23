'''Creation of the base settings object'''
import os


class Settings:
    PG_URL: str = os.environ.get('PG_URL')


settings = Settings()
