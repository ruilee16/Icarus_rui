# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 11:54:46 2021

@author: ruili
"""

import pandas as pd
import json
import pickle

from classes import route
from databaseHandler.writedata import store_data
from postprocessers import _check_wbgt_safe, calculate_exposure_2, get_link_usage, Cal_WBGT
import sqlite3
from get_link_sim_mrt import maricopa_network,daymet, daymet_dict, mrt_link, mrt_dict, LCZ_cool_mean,link_LCZ
# Create your connection.
def read_pickle(filename):
    objects = []
    with (open(filename, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects[0]


def read_route(db, tb):
    cnx = sqlite3.connect(db)
    df = pd.read_sql_query(f"SELECT * FROM {tb}", cnx)
    df['route'] = df.route.apply(json.loads)
    return [route(a.agentid, a.tripid, a.mode, a.route, a.abm_start, a.duration, a.length, a.mrt_exp, a.daymet_exp, a.wbgt_exp, a.reroute, a.vulnerable) for a in df.itertuples()]

    
s0_df = read_route(r'C:\test_codes_delete_later\db_test\db_test.db', 's0')
# some = [Cal_WBGT(i) for i in s0_df]
# _ = [_check_wbgt_safe(i) for i in s0_df]    
# store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s0_df,'s3') 
# s1_df = read_route(r'C:\test_codes_delete_later\db_test\db_test.db', 's4')
# some = [Cal_WBGT(i) for i in s1_df]
# _ = [_check_wbgt_safe(i) for i in s1_df]    
# store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s1_df,'s4') 
# s2_df = read_route(r'C:\test_codes_delete_later\db_test\db_test.db', 's5')
# some = [Cal_WBGT(i) for i in s2_df]
# _ = [_check_wbgt_safe(i) for i in s2_df]    
# store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s2_df,'s5') 

# some = [Cal_WBGT(i) for i in s2_df]
# _ = [_check_wbgt_safe(i) for i in s2_df]    
# store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s2_df,'s2') 


#_ = [calculate_exposure(i, maricopa_network,  daymet, daymet_dict, mrt_link, mrt_dict) for i in s2_df]        
s0_link_usage = get_link_usage(s0_df)
#s2_link_usage = get_link_usage(s2_df)

daymet_dict = read_pickle(r'D:\2021_ICARUS_dev\data\pickle\daymet_link_diction')
daymet_link_id = read_pickle(r'D:\2021_ICARUS_dev\data\pickle\network_daymet')
daymet = read_pickle(r'D:\2021_ICARUS_dev\data\pickle\daymet')
mrt_dict=read_pickle(r'D:\2021_ICARUS_dev\data\pickle\mrt_link_diction')
mrt_link = read_pickle(r'D:\2021_ICARUS_dev\data\pickle\mrt_parsed_onlink_dict')

maricopa_network = read_pickle(r'D:\2021_ICARUS_dev\data\pickle\maricopa_network')
for idx in mrt_dict:
    try:
        maricopa_network.links[idx]
    except:
        maricopa_network.links[idx] = maricopa_network.links.pop((idx[1], idx[0]))

hot_corridors = list(s0_link_usage[(s0_link_usage['usage']>100)]['index'])
#hot_corridors_s2 = list(s2_link_usage[(s2_link_usage['usage']>1500)]['index'])
print(sum([maricopa_network.links[i].length for i in hot_corridors]))
#links set should be a dictionary where link id (nodes), and length is in.
# write the find hot_corridor function as sum([linksets[i].length for i in hot_corridors])


some = [calculate_exposure_2(i, maricopa_network, daymet, daymet_dict, mrt_link,
                              mrt_dict, LCZ_cool_mean, hot_corridors,link_LCZ) for i in s0_df]
_ = [_check_wbgt_safe(i) for i in s0_df]
store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s0_df,'s10') 


# some = [calculate_exposure_2(i, maricopa_network,  daymet, daymet_dict, mrt_link, 
#                               mrt_dict, LCZ_cool_mean, hot_corridors_s2,link_LCZ) for i in s2_df]
# _ = [_check_wbgt_safe(i) for i in s2_df]
# store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s2_df,'s5') 



s0_df = read_route(r'C:\test_codes_delete_later\db_test\db_test.db', 's0')

some = [calculate_exposure_2(i, maricopa_network,  daymet, daymet_dict, mrt_link, 
                              mrt_dict, LCZ_cool_mean, hot_cooridors,link_LCZ) for i in s0_df]
_ = [_check_wbgt_safe(i) for i in s0_df]
store_data(r'C:\test_codes_delete_later\db_test\db_test.db', s0_df,'s3') 
'''
wbgt is dependand on humidity and not design for the desert. Taking a different approach. 
put all trips into bins and compare to how the significant the docile changes
1. send historgram of mrt 
2. check if wbgt calcultion is correct 
3. checking using the histgram 
if city took all highly vulnerable corridors, 
any any above mrt 45 C are going to be 45 C.


extreme cases. 

calculate the road way mileage 
what threashold change 


'''
