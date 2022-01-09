"""
This module would extract parcels for the start and end of each walk and bike trip. These OD were in MAZs in the ABM
data.
When selecting parcel
"""
import geopandas as gpd
import pandas as pd
import rtree
from shapely.geometry import shape
import time
import sqlite3


def __get_maz19(point, idx_retree, idx_retree_factory):
    #geo = Point(geo_x, geo_y)
    _census_blks = [n.id for n in idx_retree.intersection((point.x, point.y, point.x, point.y), objects=True)]
    for i in _census_blks:
        if idx_retree_factory[i]:
            if idx_retree_factory[i].contains(point):
                return i


def __get_idx_rtree(_maz_shp):
    idx_retree = rtree.index.Index()
    idx_retree_factory = {}
    for index, feature in _maz_shp.iterrows():
        geometry = shape(feature['geometry'])
        idx_retree.insert(index, geometry.bounds)
        idx_retree_factory[index] = geometry
    return idx_retree, idx_retree_factory


def read_parcel() -> gpd.geodataframe:
    """
    read parcel data. 
    """
    _commercial_parcel = gpd.read_file(
        r'C:\Dropbox (ASU)\Icarus\Data\Shapefiles\Maricopa Parcels\2017_Commercial_Master\2017_CommercialMaster_ALL.DBF')[['APN']]
    _commercial_parcel['parcelType'] = 'commercial'
    _residential_parcel = gpd.read_file(
        r'C:\Dropbox (ASU)\Icarus\Data\Shapefiles\Maricopa Parcels\2017_Residential_Master\2017_ResidentialMaster_All.DBF')[['APN']]
    _residential_parcel['parcelType'] = 'residential'
    _parcel_detail = _residential_parcel.append(_commercial_parcel).reset_index(drop=True).drop_duplicates()
    _parcel_shp = gpd.read_file(r'C:\Dropbox (ASU)\Icarus\Data\Shapefiles\Maricopa Parcels\Parcels_-_Maricopa_County_Arizona_(2020)\parcels_maricnty_2020.shp')[['APN', 'geometry']].dropna().head(20)
    _parcel_shp['centroid'] = _parcel_shp.centroid
    _temp_parcel = _parcel_shp.set_index('APN').join(_parcel_detail.set_index('APN')).reset_index()
    _temp_parcel.loc[_temp_parcel['parcelType'].isnull(), 'parcelType'] = 'other'
    _temp_parcel = _temp_parcel.set_geometry('centroid', drop = True)
    return _temp_parcel.dropna()


def get_maz_taz(_parcel:gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    _maz_shp = gpd.read_file(r'D:\2020 ICARUS\data\taz2019_maz2019_gisShapeFile\taz2019_maz2019_gisShapeFile\taz2019_maz2019.shp').set_index('ID')
    _maz_shp = _maz_shp.to_crs(_parcel.crs)
    idx_retree, idx_retree_factory = __get_idx_rtree(_maz_shp)
    _parcel_maz = []
    for index, row in _parcel.iterrows():
        # for index, row in temp_df.iterrows():
        _parcel_maz.append(__get_maz19(row.at['geometry'], idx_retree, idx_retree_factory))
    _parcel['MAZ'] = _parcel_maz
    _parcel.set_geometry('geometry', drop = True)
    return _parcel.groupby('APN').first().reset_index()


def get_parcel_obj(input_table, db, object_name):
    object_list_factory = []
    conn = sqlite3.connect(db)
    klass = globals()[object_name]
    dt = input_table[list(klass.__slots__)[:-1]]
    print(klass)
    object_list_factory = [klass(**kwargs) for kwargs in dt.to_dict('records')]
    # loading everything from the abm trip data would be very slow
    print('finish loading')
    conn.close()
    return object_list_factory
    
    
start = time.time()
parcels = read_parcel()
print(time.time()-start)
start = time.time()
temp = get_maz_taz(parcels)
print(time.time()-start)
start = time.time()
parcel_group = get_parcel_obj(temp, r'C:\test_codes_delete_later\sqlite\db\pythonsqlite.db', 'ParseParcel')
print(time.time()-start)
# temp_4 = temp.head(4)

store_data(r"C:\test_codes_delete_later\sqlite\db\pythonsqlite.db", parcel_group, 'parcels')

# from shapely.wkt import loads, dumps

writer = WriteIcarusObj(r"C:\test_codes_delete_later\sqlite\db\pythonsqlite.db")
writer.create_table(parcel_group, 'parcels')
writer.insert_values()
writer.close_db()

# import sqlite3
# conn = sqlite3.connect(r'C:\test_codes_delete_later\sqlite\db\pythonsqlite.db')
# temp_4.set_index('APN').to_sql(name='parse_parcels', con = conn)
