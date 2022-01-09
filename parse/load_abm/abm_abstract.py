from abc import ABC, abstractmethod
import os
import pandas as pd
from typing import List

from Classes.basic_classes import IcarusObj
from databaseHandler.writedata import store_data
from Classes.abm_classes import *
from databaseHandler.databasegeneralfunction import connect_database, check_if_table_exist


class AbmLoader(ABC):
    @abstractmethod
    def __init__(self, input_table: str, database: str) -> None:
        """return the database fields string. In the __init__ function, abm_loader module will check if the input_table
        and database exist.
        :param input_table: an url to the input abm table
        :param database: an url to the database
        :return: no return
        """

    @abstractmethod
    def ready(self) -> bool:
        """
        check if the input_table and database exist. If not, request user to update the urls.
        :return: bool. If the file exist, return true. Else, return false.
        """

    @abstractmethod
    def load_data(self) -> None:
        """
        load data from the abm tables.
        :return:
        """


class MagAbmLoader(AbmLoader):

    def __init__(self, input_table: str, database: str, object_name: str) -> None:
        self.input_table = input_table
        self.db = database
        self.object_name = object_name
        self.object_list_factory = List[IcarusObj]
        self.ready()

    def ready(self) -> bool:
        if os.path.exists(self.input_table):
            print(f'{self.input_table} exist.')
            return True
        else:
            print(f'{self.input_table} not exist.')
            return False

    def load_data(self) -> None:
        conn = connect_database(self.db)
        if check_if_table_exist(conn, self.object_name):
            print(f'{self.object_name} already exist in database, no need to load')
            return False
        else:
            print(f'{self.object_name} not exist in database,loading')
            klass = globals()[self.object_name]
            _temp_df = pd.read_csv(self.input_table, usecols=klass.__slots__)
            print(_temp_df.columns)
            self.object_list_factory = [klass(**kwargs) for kwargs in _temp_df.to_dict('records')]
            # loading everything from the abm trip data would be very slow
            print('finish loading')
            return True
        conn.close()

    def store_to_db(self) -> None:
        store_data(self.db, self.object_list_factory, self.object_name)

