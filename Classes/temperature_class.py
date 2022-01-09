from basic_classes import IcarusObj, TravelMode
from typing import List
import json


class mrt(IcarusObj):
    __slots__ = 'mrt_id', 'mrt_temperature'
    __attr_type__ = 'INT', 'TEXT'
    __primary_key__ = 'mrt_id'
    __dict_key__ = 'mrt_id'

    def __init__(self, mrt_id: int, mrt_temperature: dict):
        self.mrt_id = mrt_id
        self.mrt_temperature = mrt_temperature

    def return_values(self) -> tuple:
        return (self.mrt_id, json.dumps(self.mrt_temperature))


class Daymet(IcarusObj):
    __slots__ = 'daymet_id', 'daymet_temperature'
    __attr_type__ = 'INT', 'TEXT'
    __primary_key__ = 'daymet_id'
    __dict_key__ = 'daymet_id'

    def __init__(self, daymet_id: int, daymet_temperature: dict):
        self.daymet_id = daymet_id
        self.daymet_temperature = daymet_temperature

    def return_values(self) -> tuple:
        return (self.daymet_id, json.dumps(self.daymet_temperature))
