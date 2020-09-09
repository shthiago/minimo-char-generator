'''Database models specification'''

from dataclasses import dataclass
from typing import List, Any

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings


if not settings.TESTING:  # pragma: no cover
    url = settings.DB_URL

else:  # pragma: no cover
    url = settings.TEST_DB_URL

if not url:  # pragma: no cover
    raise Exception('URL not set at environment')

engine = create_engine(url, echo=True)
Base: Any = declarative_base()


class Theme(Base):  # pragma: no cover
    '''Object to hold information about themes'''
    __tablename__ = 'theme'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    def __init__(self, name: str) -> None:
        '''Init theme'''
        self.name = name


class Name(Base):  # pragma: no cover
    '''Object to hold information about names for characters'''
    __tablename__ = 'name'
    gender_values = tuple(settings.CHARACTER_GENDER_POSSIBILITIES)
    __table_args__ = (
        CheckConstraint(f'gender IN {gender_values}'),
        UniqueConstraint('firstname', 'lastname')
    )

    id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    gender = Column(String(9), nullable=False)

    def __init__(self, firstname: str, lastname: str, gender: str) -> None:
        '''Init feature'''
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender


class Feature(Base):  # pragma: no cover
    '''Object to hold information about characters feature'''
    __tablename__ = 'feature'

    id = Column(Integer, primary_key=True)
    text_masc = Column(String(20), nullable=False, unique=True)
    text_fem = Column(String(20), nullable=False, unique=True)
    description = Column(String(200), nullable=True)
    is_good = Column(Boolean, nullable=False)

    def __init__(self, text_masc: str, text_fem: str,
                 is_good: bool, description: str) -> None:
        '''Init feature'''
        self.text_masc = text_masc
        self.text_fem = text_fem
        self.description = description
        self.is_good = is_good


class Item(Base):  # pragma: no cover
    '''Object to hold information about equipments the character can carry'''
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(200), nullable=False)

    def __init__(self, name: str) -> None:
        '''Init item'''
        self.name = name


class LinkItemTheme(Base):  # pragma: no cover
    '''Object to associate a item with theme, many to many relation'''
    __tablename__ = 'linkitemtheme'
    __table_args__ = (
        UniqueConstraint('id_item', 'id_theme'),
    )

    id = Column(Integer, primary_key=True)
    id_theme = Column(Integer, ForeignKey('theme.id'), nullable=False)
    id_item = Column(Integer, ForeignKey('item.id'), nullable=False)

    def __init__(self, id_theme: int, id_item: int) -> None:
        '''init link'''
        self.id_theme = id_theme
        self.id_ = id_item


class LinkNameTheme(Base):  # pragma: no cover
    '''Object to associate a name with theme, many to many relation'''
    __tablename__ = 'linknametheme'
    __table_args__ = (
        UniqueConstraint('id_name', 'id_theme'),
    )

    id = Column(Integer, primary_key=True)
    id_theme = Column(Integer, ForeignKey('theme.id'), nullable=False)
    id_name = Column(Integer, ForeignKey('name.id'), nullable=False)

    def __init__(self, id_theme: int, id_name: int) -> None:
        '''init link'''
        self.id_theme = id_theme
        self.id_name = id_name


class LinkFeatureTheme(Base):  # pragma: no cover
    '''Object to associate a feature with theme, many to many relation'''
    __tablename__ = 'linkfeaturetheme'
    __table_args__ = (
        UniqueConstraint('id_feature', 'id_theme'),
    )

    id = Column(Integer, primary_key=True)
    id_theme = Column(Integer, ForeignKey('theme.id'), nullable=False)
    id_feature = Column(Integer, ForeignKey('feature.id'), nullable=False)

    def __init__(self, id_theme: int, id_feature: int) -> None:
        '''init link'''
        self.id_theme = id_theme
        self.id_feature = id_feature


# Dataclasses to orient insertin functions


@dataclass
class NameInput:
    '''A model for name input, in populating names

    Attributes:
        firstname: character first name
        lastname: character last name, can be null
        gender: masculine, feminine or neutral
        themes: list of theme ids
    '''
    firstname: str
    lastname: str
    gender: str
    themes: List[str]


@dataclass
class ItemInput:
    '''A model for item input

    Attributes:
        name: item name
        description: description for item
        themes: list of theme ids
    '''
    name: str
    description: str
    themes: List[str]


@dataclass
class FeatureInput:
    '''A model for feature input

    Attributes:
        text_masc: masculine text
        text_fem: feminine text
        description: description of the feature
        is_good: is a good feature or a bad one
    '''
    text_masc: str
    text_fem: str
    description: str
    is_good: str
    themes: List[str]


@dataclass
class LoadedDbItemsJson:
    '''A model for loaded input from JSON

    Attributs:
        themes: list of theme names
        items: list of ItemInput
        names: list of NameInput
    '''

    themes: List[str]
    items: List[ItemInput]
    names: List[NameInput]
    features: List[FeatureInput]
