"""
This module would extract parcels for the start and end of each walk and bike trip. These OD were in MAZs in the ABM
data.
When selecting parcel
"""
import geopandas as gpd
import pandas as pd
import rtree
import sqlite3
from typing import List

from Classes.basic_classes import IcarusObj
from databaseHandler.databasegeneralfunction import connect_database, check_if_table_exist
from utils.rtrees.rtree_processor import *

__all__ = ['read_parcel', 'get_maz', 'get_parcel_obj']

def read_parcel() -> gpd.geodataframe:
    """
    read parcel data
    :return: parcel data with parcel type and MAZ
    """
    _commercial_parcel = gpd.read_file(
        r'C:\Dropbox (ASU)\Icarus\Data\Shapefiles\Maricopa Parcels\2017_Commercial_Master\2017_CommercialMaster_ALL.DBF')[['APN']]
    _commercial_parcel['parcelType'] = 'commercial'
    _residential_parcel = gpd.read_file(
        r'C:\Dropbox (ASU)\Icarus\Data\Shapefiles\Maricopa Parcels\2017_Residential_Master\2017_ResidentialMaster_All.DBF')[['APN']]
    _residential_parcel['parcelType'] = 'residential'
    _parcel_detail = _residential_parcel.append(_commercial_parcel).reset_index(drop=True).drop_duplicates()
    _parcel_shp = gpd.read_file(r'C:\Dropbox (ASU)\Icarus\Data\Shapefiles\Maricopa Parcels\Parcels_-_Maricopa_County_Arizona_(2020)\parcels_maricnty_2020.shp')[['APN', 'geometry']].dropna()
    _parcel_shp['centroid'] = _parcel_shp.centroid
    _temp_parcel = _parcel_shp.set_index('APN').join(_parcel_detail.set_index('APN')).reset_index()
    _temp_parcel.loc[_temp_parcel['parcelType'].isnull(), 'parcelType'] = 'other'
    _temp_parcel.set_geometry('centroid', drop = True)
    return _temp_parcel.groupby('APN').first().reset_index()


def get_maz(parcel: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    _maz_shp = gpd.read_file(
        r'D:\2020 ICARUS\data\taz2019_maz2019_gisShapeFile\taz2019_maz2019_gisShapeFile\taz2019_maz2019.shp').set_index(
        'ID')
    _maz_shp = _maz_shp.to_crs(parcel.crs)
    idx_rtree, idx_rtree_factory = _get_idx_rtree(_maz_shp)
    _parcel_maz = []
    for index, row in parcel.iterrows():
        _parcel_maz.append(_get_idx(row.at['geometry'], idx_rtree, idx_rtree_factory))
    parcel['MAZ'] = _parcel_maz
    return parcel.dropna()


def get_parcel_obj(input_table, db, object_name) -> List[IcarusObj]:
    """
    take the parcel geometry in, and return
    :param input_table:
    :param db:
    :param object_name:
    :return:
    """
    object_list_factory = List[IcarusObj]
    conn = sqlite3.connect(db)

    if check_if_table_exist(conn, object_name):
        print(f'{object_name} already exist in database, no need to load')
        return False
    else:
        print(f'{object_name} not exist in database,loading')
        klass = globals()[object_name]
        dt = input_table[list(klass.__slots__)[: -1]]
        object_list_factory = [klass(**kwargs) for kwargs in dt.to_dict('records')]
        # loading everything from the abm trip data would be very slow
        print('finish loading')
        return True
    conn.close()
    return object_list_factory

