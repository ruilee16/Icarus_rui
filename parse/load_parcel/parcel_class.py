from shapely.geometry import Point
from shapely.wkt import dumps

from Classes.basic_classes import IcarusObj

__all__ = ['ParseParcel']


class ParseParcel(IcarusObj):
    """read in the parcel data and generate Parcel objective."""
    __slots__ = 'APN', 'MAZ', 'parcelType', 'geometry', 'nearNode'
    __attr_type__ = 'INT', 'INT', 'VARCHAR', 'VARCHAR', 'INT'
    __primary_key__ = 'APN'
    __dict_key__ = 'APN'

    def __init__(self, APN: int, MAZ: int, parcelType: str, geometry: Point, nearNode: int = None):
        """

        :param APN:
        :param MAZ:
        :param parcelType:
        :param geometry:
        :param nearNode:
        """
        self.APN = APN
        self.MAZ = MAZ
        self.parcelType = parcelType
        self.geometry = geometry
        self.nearNode = nearNode

    def dict_id(self) -> int:
        """
        return the dictionary key link to the abm_household object
        :return: return hhid (Household ID) as key
        """
        return self.APN

    def return_values(self) -> tuple:
        # rewrite return_values function in the icarus_obj object
        return (self.APN, self.MAZ, self.parcelType, dumps(self.geometry), self.nearNode)

