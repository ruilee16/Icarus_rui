from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty
from basic_classes import TravelMode

class Trip(ABC):
    # abstract class should only have abstract methods
    @abstractmethod
    def __init__(self):...



class activeTrip(Trip):
    def __init__(self):
        self.abm_start = abm_start
        self.abm_end = abm_end
        self.routes = None
        self.length = None
        self.exp = 26.6 * (abm_end - abm_start) / 60 if mode == 'car' else None
        self.activity_start = None
        self.activity_end = None


class vehicleTrip(Trip):
    def __init__(self): ...


class walking(activeTrip):
    def __init__(self):
        self.mode = TravelMode(1)
    pass

class biking(activeTrip):
    def __init__(self):
        self.mode = TravelMode(2)

class car(vehicleTrip):
    def __init__(self):
        self.mode = TravelMode(4)

class bus(vehicleTrip):
    def __init__(self):
        self.mode = TravelMode(3)