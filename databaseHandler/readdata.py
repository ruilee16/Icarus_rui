"""
data reader is a module that read data from sqlite3 database, and export the data in dataframe or object structure.
The main purpose of datareader is to give an easy way to creat objects defined in the Classes.classes from the database.
The abstract class Fetcher defines the basic structure of a data fetcher. Users can use inheritance to define their own
data fetcher.


"""

import sqlite3
from abc import ABC, abstractmethod
import pandas as pd
import json


from Classes.classes import *


class Fetcher(ABC):
    def __init__(self, db_name: str) -> None:
        self.con = sqlite3.connect(db_name)
        """initialize data fetcher with the database name and connection
        :param db_name: database url and name
        """

    @abstractmethod
    def fetch_data_to_obj(self, table_name: str, object_name: str) -> list:
        """
        fetch data in the database to objects.
        :param table_name: the stored table name in the database
        :param object_name: the object name users wish to fetch to
        :return: return a list of objects
        """

    def fetch_data_to_df(self, table_name: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {table_name}", self.con)
        """
        fetch data in the database to dataframe.
        :param table_name: the stored table name in the database
        :return: return the fetched dataframe
        """


class ResultFetcher(Fetcher):
    def fetch_data_to_obj(self, table_name: str, object_name: str = 'Route') -> list:
        temp_df = self.fetch_data_to_df(table_name)
        temp_df['route'] = temp_df.route.apply(json.loads)
        return [Route(a.agentid, a.tripid, a.mode, a.route, a.abm_start, a.duration, a.length, a.mrt_exp, a.daymet_exp,
                      a.wbgt_exp, a.reroute, a.vulnerable) for a in temp_df.itertuples()]


class LinkFetcher(Fetcher):
    def fetch_data_to_obj(self, table_name: str = 'links', object_name: str = 'Link') -> list:
        temp_df = self.fetch_data_to_df(table_name)
        return [Link(a.node1, a.node2, a.length) for a in temp_df.itertuples()]
