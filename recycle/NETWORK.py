from abc import ABC, abstractmethod
import networkx as nx

class network(ABC):
    @abstractmethod
    def read_data_from_db(self, db):
        """Get links and nodes data from database"""
        pass

    @abstractmethod
    def generate_graph_with_weight(self) -> nx.Graph:
        """Generate Networkx network graph which can be routed"""
        pass

class network_with_env(ABC):
    pass