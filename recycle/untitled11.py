# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 16:45:19 2021

@author: ruili
"""
import sqlite3
from abc import ABC, abstractmethod
import os

class abm_loader(ABC):
    @abstractmethod
    def __init__(self, input_table: str, database: str) -> None:
        """return the database fields string. In the __init__ function, abm_loader module will check if the input_table and database exist.
        :param input_table: an url to the input abm table
        :param database: an url to the database
        :return: no return
        """

    @abstractmethod
    def ready(self) -> None:
        """
        check if the input_table and database exist. If not, request user to update the urls.
        :return:
        """

    @abstractmethod
    def __del__(self) -> None:
        """
        delete object
        :return:
        """

class MAG_abm_loader(abm_loader):

    def __init__(self, input_table: str, database: str) -> None:
        self.input_table = input_table
        self.db = database
        self.ready()


    def ready(self) -> None:
        if os.path.exists(self.input_table):
            print(f'{self.input_table} exist.')
        else:
            self.__del__()


    def __del__(self) -> None:
        print('file not exist. Please reload file.')