from __future__ import annotations

from typing import Iterable
from enum import Enum
from abc import ABC, abstractmethod


class TravelMode(Enum):
    WALK = 1
    BIKE = 2
    BUS = 3
    CAR = 4


class IcarusObj(ABC):
    __attr_type__: str | Iterable[str]
    __primary_key__: str | Iterable[str]
    __dict_key__: str | Iterable[str]

    def database_fields(self) -> str:
        """
        return the database fields string
        :returns a string used for create database field. Distinguish the method between one and multiple primary keys.
        """
        if isinstance(self.__primary_key__, str):
            return ', '.join([f'{i[0]} {i[1]}' for i in zip(self.__slots__, self.__attr_type__)]) + ', PRIMARY KEY (' \
                   + self.__primary_key__ + ')'
        else:
            return ', '.join([f'{i[0]} {i[1]}' for i in zip(self.__slots__, self.__attr_type__)]) + ', PRIMARY KEY (' \
                   + ', '.join(self.__primary_key__) + ')'

    def return_values(self) -> tuple:
        """
        return the value of object, which will be used to store in the database. The default function is slow. Users can
        override this function
        :return: tuple of values
        """
        return tuple(getattr(self, i) for i in self.__slots__)

    @abstractmethod
    def dict_id(self) -> object:
        """
        return the value of object as
        :returns a string used in sql query
        """
