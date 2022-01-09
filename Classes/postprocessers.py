from classes import route
import pandas as pd
from pylab import *
from typing import List


def get_link_flow():
    pass


def calculate_globe_temperature():
    pass


def calculate_NWB(trip, RH):
    NWB = -5.806 + 0.672 * trip.daymet_exp - 0.006 * trip.daymet_exp ** 2 + \
          (0.061 + 0.004 * trip.daymet_exp + 99 * 10 ** (-6) * trip.daymet_exp ** 2) * RH * 100- \
          (33 * 10 ** (-6) + 5 * 10 ** (-6) * trip.daymet_exp + 1 * 10 ** (-7) * trip.daymet_exp ** 2) * (RH*100 ** 2)
    return NWB


def calculate_NWB_1(trip, RH):
    NWB = trip.daymet_exp * math.atan(0.151977 * ((RH * 100 + 8.313659) ** (1 / 2))) + math.atan(
        (trip.daymet_exp + RH * 100)) - math.atan(RH * 100 - 1.676331) + 0.00391838 * ((RH * 100) ** (3 / 2)) * math.atan(
        0.023101 * RH * 100) - 4.686035  # Stull 2011 method. Calculation checked
    return NWB


def calculate_GT(trip, Va):
    # solve Ts_bar: (Ts_bar + 273.15)^4+p[3](Ts_bar+273.15)+P[4]=0
    '''
    alpha = (0.24 + 2.08 * (Va ** 0.5) + 1.14 * (Va ** 0.667)) * (10 ** 8)
    if math.isnan(trip.mrt_exp):
        trip.mrt_exp = 60
    belta = -alpha * 273.15 - alpha * trip.daymet_exp - (trip.mrt_exp + 273.15) ** 4
    '''
    p_3 = 6 * Va ** 0.466*10**8
    p_4 = -(trip.daymet_exp+273.15)*10**8*6*Va**0.466-(trip.mrt_exp+273.15)**4
    #print([1, 0, 0, p_3, p_4])
    r = roots([1, 0, 0, p_3, p_4])
    #print(r)
    Ts_bar = r[(r.imag == 0) & (r.real >= 0)].real.min() - 273.15
    mrt =((Ts_bar+273.15)**4 + 6*Va**0.466*(Ts_bar-trip.daymet_exp)*10**8)**0.25-273.15
    #print(f'{trip.mrt_exp},{mrt}')
    GT = (Ts_bar - 0.725 + 0.369*trip.daymet_exp)/1.345
    return GT


def calculate_GT_1(trip, Va):
    # solve Ts_bar: (Ts_bar + 273.15)^4+p[3](Ts_bar+273.15)+P[4]=0
    '''
    alpha = (0.24 + 2.08 * (Va ** 0.5) + 1.14 * (Va ** 0.667)) * (10 ** 8)
    if math.isnan(trip.mrt_exp):
        trip.mrt_exp = 60
    belta = -alpha * 273.15 - alpha * trip.daymet_exp - (trip.mrt_exp + 273.15) ** 4
    '''
    p_3 = (0.24+2.08*Va**0.5+1.14*Va**0.667)*10**8
    p_4 = -(trip.daymet_exp+273.15)*(0.24+2.08*Va**0.5+1.14*Va**0.667)*10**8-(trip.mrt_exp+273.15)**4
    #print([1, 0, 0, p_3, p_4])
    r = roots([1, 0, 0, p_3, p_4])
    #print(r)
    Ts_bar = r[(r.imag == 0) & (r.real >= 0)].real.min() - 273.15
    mrt =((Ts_bar+273.15)**4 + (0.24+2.08*Va**0.5+1.14*Va**0.667)*10**8*(Ts_bar-trip.daymet_exp))**0.25-273.15
    #print(f'{trip.mrt_exp},{mrt}')
    GT = (Ts_bar - 0.725 + 0.369*trip.daymet_exp)/1.345
    return GT


def Cal_WBGT(trip, RH: float = 0.2, Va: float = 3.2, outdoor: bool =True):
    '''
    Calculate WBGT using Vanos et al., 2021, Skull 2011, and Dimiceli & Piltz n.d. method.

    :param trip:
    :param RH: Relative Humidity (assume to be 20% in June @ Phoenix)
    :param Va:
    :param outdoor: 
    :return: 
    
    WBGT calculation: for outdoors with direct sun exposure:
        WBGT = 0.7*NWB + 0.2*Temp_globe + 0.1*Temp_air
    for indoors and outdoors without direct sun exposure:
        WBGT = 0.7*NWB + 0.3*Temp_globe
            NWB: nature wet-bulb temperature (using Daymet and Humidity to esitiamte GT from Stull 2011) https://journals-ametsoc-org.ezproxy1.lib.asu.edu/view/journals/apme/50/11/jamc-d-11-0143.1.xml
                or: method 2
            GT: Globe Temperature (using MRT to estimate GT Vanos et al., 2021)
            DB: dry bulb temperature. Here assuming DB equals to air temperature equals to Daymet temperature
    '''
    NWB = calculate_NWB_1(trip, RH)
    '''
        NWB = trip.daymet_exp * math.atan(0.151977 * ((RH * 100 + 8.313659) ** (1 / 2))) + math.atan(
            (trip.daymet_exp + RH * 100)) - math.atan(RH * 100 - 1.676331) + 0.00391838 * ((RH * 100) ** (3 / 2)) * math.atan(
            0.023101 * RH * 100) - 4.686035 # Stull 2011 method        
    '''

        # (Ts+273.15)^4+alpha*(Ts+273.15)+belta = 0
    GT = calculate_GT_1(trip, Va)
    # DB: dry bulb temperature. Here assuming DB equals to air temperature
    DB = trip.daymet_exp
    if trip.mrt_exp == trip.daymet_exp : outdoor = False
    if outdoor:
        # outdoor calculation
        trip.wbgt_exp = 0.7 * NWB + 0.2 * GT + 0.1 * DB
        #print(f'NWB: {NWB}, GT: {GT}, DB: {DB}, WBGT: {trip.wbgt_exp}')
    else:
        # indoor calculation
        trip.wbgt_exp = 0.7 * NWB + 0.3 * GT

def calculate_exposure(trip: route, network_data, daymet, daymet_dict, mrt_link, mrt_dict):

        start_step = trip.abm_start / 60 // 15 * 15
        
        if (trip.mode in ('walk', 'bike')) and len(trip.route)>1:
        
            link_list = list(zip(trip.route[0:-1], trip.route[1:]))
            # steps = dur//15
            link_list = set([tuple(sorted(i)) for i in link_list])
            
            try:
                _temp_daymet = [daymet[daymet_dict[i]][start_step] for i in link_list]

                _temp_length = [network_data.links[i].length for i in link_list]

                trip.length = sum(_temp_length)
                trip.daymet_exp = sum([a * b for a, b in zip(_temp_daymet, _temp_length)]) / sum(_temp_length)
                try:
                    _temp_temperatue = [mrt_link[mrt_dict[i]].temp[start_step] for i in link_list]
                    trip.mrt_exp = sum([a * b for a, b in zip(_temp_temperatue, _temp_length)]) / sum(_temp_length)
                    Cal_WBGT(trip,0.2, 3.2)

                except:
                    trip.mrt_exp = trip.daymet_exp
                    Cal_WBGT(trip, 0.2, 3.2)
            except:
                pass


def get_link_usage(trips : List):
    _link_usage = {}
    for trip in trips:
        if len(trip.route)>1:
            link_list = list(zip(trip.route[0:-1], trip.route[1:]))
            link_list = [tuple(sorted(i)) for i in link_list]
            for link in link_list:
                if link in _link_usage:
                    _link_usage[link] += 1
                else:
                    _link_usage[link] = 1
    return pd.DataFrame.from_dict(_link_usage, orient='index', columns=['usage']).reset_index()


def calculate_exposure_2(trip: route, network_data, mrt_link, mrt_dict, mrt_temp, hot_coor_list, link_LCZ):
    start_step = trip.abm_start / 60 // 15 * 15

    if (trip.mode in ('walk', 'bike')) and len(trip.route) > 1:

        link_list = list(zip(trip.route[0:-1], trip.route[1:]))
        # steps = dur//15
        link_list = set([tuple(sorted(i)) for i in link_list])
        try:
            hot_links = list(link_list & set(hot_coor_list))
            if len(hot_links)>0:
                try:

                    _temp_length = [network_data.links[i].length for i in link_list]
                    _temp_temperatue = [mrt_temp[link_LCZ[i]].temp[start_step] if (i in hot_links) else mrt_link[mrt_dict[i]].temp[start_step] for i in link_list ]
                    trip.mrt_exp = sum([a * b for a, b in zip(_temp_temperatue, _temp_length)]) / sum(_temp_length)
                    Cal_WBGT(trip, 0.2, 3.2)
                    trip.reroute = trip.reroute+10
                    # if reroute tag is 10, it means this trip temperature changed after environmental change
                except:
                    pass
        except:
            pass


def _check_wbgt_safe(trip: route):
    try:
        if trip.mode == 'walk':
            if  26<= trip.wbgt_exp < 29:
                if trip.duration > 50*60:
                    trip.vulnerable = 1
            elif 29 <= trip.wbgt_exp < 31:
                if trip.duration > 40*60:
                    trip.vulnerable = 1
            elif 31 <= trip.wbgt_exp < 32:
                if trip.duration > 30*60:
                    trip.vulnerable = 1
            elif 32 <= trip.wbgt_exp < 36:
                if trip.duration > 20*60:
                    trip.vulnerable = 1
            elif trip.wbgt_exp>= 36:
                trip.vulnerable = 1
            else:
                trip.vulnerable = 0
        elif trip.mode == 'bike':
            if 26<= trip.wbgt_exp < 29:
                if trip.duration > 40*60:
                    trip.vulnerable = 1
            elif 29 <= trip.wbgt_exp < 31:
                if trip.duration > 30*60:
                    trip.vulnerable = 1
            elif 31 <= trip.wbgt_exp < 32:
                if trip.duration > 20*60:
                    trip.vulnerable = 1
            elif 32 <= trip.wbgt_exp < 36:
                if trip.duration > 10*60:
                    trip.vulnerable = 1
            elif trip.wbgt_exp >= 36:
                trip.vulnerable = 1
            else:
                trip.vulnerable = 0

    except:
        trip.vulnerable = 0
    return trip.vulnerable
