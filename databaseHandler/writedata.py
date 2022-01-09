from abc import ABC, abstractmethod
from typing import List

from databaseHandler.databasegeneralfunction import connect_database
from Classes.basic_classes import IcarusObj


class DataWriter(ABC):

    @abstractmethod
    def __init__(self, db_name: str):
        """initialize data fetcher with the database name and connection
        :param db_name: database url and name
        """
        self.conn = connect_database(db_name)

    @abstractmethod
    def create_table(self, network_data: List[IcarusObj], tb_name: str):
        """fetch data from the database"""

    @abstractmethod
    def insert_values(self, tb_name: str, data_values: list):
        pass

    def close_db(self) -> None:
        self.conn.close()


class WriteIcarusObj(DataWriter):
    def __init__(self, db_name: str):
        self.conn = connect_database(db_name)

    def create_table(self, network_data: List[IcarusObj], table_name: str) -> None:
        #_nodes_query = '''CREATE TABLE IF NOT EXISTS nodes (osm_id INT, x FLOAT, y FLOAT,  PRIMARY KEY (osm_id));'''
        #self.conn.cursor.execute(_nodes_query)
        self.data = network_data
        self.table_name = table_name
        # delete table if already exist.
        self.conn.cursor().execute(f"DROP TABLE IF EXISTS {self.table_name};")
        _links_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({self.data[0].database_fields()});"
        print(_links_query)
        #print(_links_query)
        self.conn.cursor().execute(_links_query)
        self.conn.commit()

    def insert_values(self):
        __temp = len(self.data[0].__slots__)
        #_insert_query = f"INSERT INTO {type(self.data[0]).__name__} VALUES({','.join('?'*len(self.data[0].__slots__))})"
        _insert_query = f"INSERT INTO {self.table_name} VALUES({','.join('?'*len(self.data[0].__slots__))})"
        value = tuple(i.return_values() for i in self.data)
        self.conn.cursor().executemany(_insert_query, value)
        self.conn.commit()


def store_data(db_name: str, dt: List[IcarusObj], tb_name: str):
    """
    write IcarusObject into database
    :param db_name:
    :param dt:
    :param tb_name:
    :return:
    """
    writer = WriteIcarusObj(db_name)
    writer.create_table(dt, tb_name)
    writer.insert_values()
    writer.close_db()
