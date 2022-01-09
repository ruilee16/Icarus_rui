from abc import ABC, abstractmethod
class node(ABC):
    @abstractmethod
    def __init__(self, osm_id: int, x: float, y: float):
        pass

    @abstractmethod
    def to_dict(self):
        pass

class