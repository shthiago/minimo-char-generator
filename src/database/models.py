import os

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


uri = os.environ.get('PG_URI', False)
if not uri:
    raise Exception('PG_URI not set at environment')

engine = create_engine(uri, echo=True)
Base = declarative_base()


class Theme(Base):
    '''Object to hold information about themes'''
    __tablename__ = 'theme'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __init__(self, name: str) -> None:
        '''Init theme'''
        self.name = name


class Name(Base):
    '''Object to hold information about names for characters'''
    __tablename__ = 'name'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20))
    id_theme = Column(Integer, ForeignKey('theme.id'), nullable=False)

    def __init__(self, firstname: str, lastname: str, id_theme: int) -> None:
        '''Init feature'''
        self.firstname = firstname
        self.lastname = lastname
        self.id_theme = id_theme


class Feature(Base):
    '''Object to hold information about characters feature'''
    __tablename__ = 'feature'

    id = Column(Integer, primary_key=True)
    text = Column(String(20), nullable=False)
    is_good = Column(Boolean, nullable=False)
    id_theme = Column(Integer, ForeignKey('theme.id'), nullable=False)

    def __init__(self, text: str, is_good: bool, id_theme: int) -> None:
        '''Init feature'''
        self.text = text
        self.is_good = is_good
        self.id_theme


class Item(Base):
    '''Object to hold information about equipments the character can carry'''
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    id_theme = Column(Integer, ForeignKey('theme.id'), nullable=False)

    def __init__(self, name: str, id_theme: int) -> None:
        '''Init item'''
        self.name = name
        self.id_theme = id_theme
