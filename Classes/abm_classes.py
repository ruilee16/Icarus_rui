""" classes to hold ABM household, agent, and trip data"""

from enum import Enum

from Classes.basic_classes import IcarusObj


__all__ = ['AbmTrip', 'AbmPerson', 'AbmHousehold']


class AbmHousehold(IcarusObj):
    """read in the abm_household data and generate abm_household objective."""
    __slots__ = 'hhid', 'homeTAZ', 'homeMaz', 'hhsize', 'hhIncomeDollars'
    __attr_type__ = 'INT', 'INT', 'INT', 'INT', 'INT', 'INT'
    __primary_key__ = 'hhid'
    __dict_key__ = 'hhid'

    def __init__(self, hhid: int, homeTAZ: int, homeMaz: int, hhsize: int, hhIncomeDollars: int):
        """ initialize an abm_household object from the data
        :param hhid: Household ID
        :param homeTAZ: Home TAZ
        :param homeMaz: Home MAZ
        :param hhsize: Household size, how many people in a household
        :param hhIncomeDollars: Household income, $
        """
        self.hhid = hhid
        self.homeTAZ = homeTAZ
        self.homeMaz = homeMaz
        self.hhsize = hhsize
        self.hhIncomeDollars = hhIncomeDollars

    def dict_id(self) -> int:
        """
        return the dictionary key link to the abm_household object
        :return: return hhid (Household ID) as key
        """
        return self.hhid


class AbmPerson(IcarusObj):
    class PersType(Enum):
        Full_time_worker = 1
        Part_time_worker = 2
        University_student = 3
        Non_worker = 4
        Retiree = 5
        Driving_age_school_child = 6
        Pre_driving_age_school_child = 7
        Preschool_child = 8

    __slots__ = 'hhid', 'pnum', 'persType', 'age', 'gender'
    __attr_type__ = 'INT', 'INT', 'INT', 'INT', 'INT'
    __primary_key__ = 'hhid', 'pnum'
    __dict_key__ = 'hhid', 'pnum'

    def __init__(self, hhid: int, pnum: int, persType: int, age: int, gender: int):
        self.hhid = hhid
        self.pnum = pnum
        self.persType = persType
        self.age = age
        self.gender = gender

    def dict_id(self) -> tuple:
        _dict_temp = (self.hhid, self.pnum)
        return _dict_temp


class AbmTrip(IcarusObj):

    __slots__ = 'hhid', 'pnum', 'personTripNum', 'origTaz', 'origMaz', 'destTaz', 'destMaz', 'origPurp', 'destPurp', \
                'isamAdjDepMin', 'isamAdjArrMin', 'isamAdjDurMin', 'mode'
    __attr_type__ = 'INT', 'INT', 'INT', 'INT', 'INT', 'INT', 'INT', 'INT', 'INT', 'FLOAT', 'FLOAT', 'FLOAT', 'INT'
    __primary_key__ = 'hhid', 'pnum', 'personTripNum'
    __dict_key__ = 'hhid', 'pnum', 'personTripNum'

    def __init__(self, hhid: int, pnum: int, personTripNum: int, origTaz: int = None, origMaz: int = None,
                 destTaz: int = None, destMaz: int = None, origPurp: int = None, destPurp: int = None,
                 isamAdjDepMin: float = None, isamAdjArrMin: float = None, isamAdjDurMin: float = None,
                 mode: int = None):
        """

        :param hhid:
        :param pnum:
        :param personTripNum:
        :param origTaz:
        :param origMaz: corresponding to MAZ_SNO in the taz2019_maz2019 file
        :param destTaz:
        :param destMaz:
        :param origPurp:
        :param destPurp:
        :param isamAdjDepMin:
        :param isamAdjArrMin:
        :param isamAdjDurMin:
        :param mode:
        """
        self.hhid = hhid
        self.pnum = pnum
        self.personTripNum = personTripNum
        self.origTaz = origTaz
        self.origMaz = origMaz
        self.destTaz = destTaz
        self.destMaz = destMaz
        self.origPurp = origPurp
        self.destPurp = destPurp
        self.isamAdjDepMin = isamAdjDepMin
        self.isamAdjArrMin = isamAdjArrMin
        self.isamAdjDurMin = isamAdjDurMin
        self.mode = mode

    def dict_id(self) -> tuple:
        _dict_temp = (self.hhid, self.pnum, self.personTripNum)
        return _dict_temp
