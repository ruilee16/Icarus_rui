"""
This module would extract parcels for the start and end of each walk and bike trip. These OD were in MAZs in the ABM
data.
Notice: this process is very slow. average time would be 10 minutes to finish process. Most time spend on loading the
parcels and idenity MAZ on parcels.
"""

from load_parcel.parcel_reader import *
import time
from databaseHandler.writedata import store_data

start = time.time()
parcels = read_parcel() # about 3 minutes
print(parcels.columns)
print(time.time()-start)
temp = get_maz(parcels)
print(time.time()-start)
parcel_factory = get_parcel_obj(temp, r'C:\test_codes_delete_later\sqlite\db\pythonsqlite.db', 'ParseParcel')
print(time.time()-start)

store_data(r"C:\test_codes_delete_later\db_test\db_test.db", parcel_factory, 'parcels')
# next is store parcel in db.