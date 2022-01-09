# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:42:54 2021

@author: ruili
"""
from Classes.basic_classes import IcarusObj, TravelMode
from typing import List
import json

__all__ = ['Node', 'Link', 'Trip', 'Route']


class Node(IcarusObj):
    __slots__ = 'node_id', 'x', 'y'
    __attr_type__ = 'INT', 'FLOAT', 'FLOAT' # move this to dataset class
    __primary_key__ = 'node_id'
    __dict_key__ = 'node_id'

    def __init__(self, node_id: int, x: float = 0, y: int = 0):
        self.node_id = node_id
        self.x = x
        self.y = y
        #self.length = geodesic((node[0].geometry.y, node[0].geometry.x), (node[1].geometry.y, node[1].geometry.x)).kilometers*1000

    # the calculation of link length can be done outs_ide of link object. (and better to be done outs_ide)
    def dict_id(self):
        return self.node_id


class Link(IcarusObj):
    __slots__ = 'node1', 'node2', 'osm_id', 'length', 'mrt_id', 'daymet_id'
    __attr_type__ = 'INT', 'INT', 'INT', 'FLOAT', 'INT', 'INT' # move this to dataset class
    __primary_key__ = 'node1', 'node2'
    __dict_key__ = ('node1', 'node2')

    def __init__(self, node1: int = 0, node2: int = 0, length: float = 0, osm_id: int = 0, mrt_id: int = 0, daymet_id: int = 0):
        self.node1 = min(node1, node2) #if all((node1, node2)) else 0 
        self.node2 = max(node1, node2) #if all((node1, node2)) else 0
        self.length = length
        #self.length = geodesic((node[0].geometry.y, node[0].geometry.x), (node[1].geometry.y, node[1].geometry.x)).kilometers*1000
        self.osm_id = osm_id
        self.mrt_id = mrt_id
        self.daymet_id = daymet_id

    # the calculation of link length can be done outs_ide of link object. (and better to be done outs_ide)
    def dict_id(self):
        return (self.node1, self.node2)


class Trip(IcarusObj):
    __slots__ = 'agent_id', 'trip_id', 'trip_start', 'trip_end', 'mode'
    __attr_type__ = 'INT', 'INT', 'INT', 'INT', 'STRING' 
    __primary_key__ = 'agent_id', 'trip_id'
    __dict_key__ = 'trip_id'
    
    def __init__(self, agent_id: int, trip_id: int, trip_start: int, trip_end: int, mode: object):
        self.agent_id = agent_id
        self.trip_id = trip_id
        self.trip_start = trip_start
        self.trip_end = trip_end
        self.mode = mode if isinstance(mode, str) else TravelMode(mode)

    def dict_id(self):
        return self.trip_id


class Route(IcarusObj):
    __slots__ = 'agent_id', 'trip_id', 'mode', 'route', 'abm_start', 'duration', 'length', 'mrt_exp', 'daymet_exp', \
                'wbgt_exp', 'reroute', 'vulnerable'
    __attr_type__ = 'INT', 'INT', 'VARCHAR', 'VARCHAR', 'INT', 'INT', 'FLOAT', 'FLOAT', 'FLOAT', 'FLOAT', 'INT', 'INT'
    __primary_key__ = 'agent_id', 'trip_id'
    __dict_key__ = 'trip_id'
    
    def __init__(self, agent_id: int = 0, trip_id: int = 0, mode:str = 'walk', route: List[int] = 0, abm_start: int = 0, duration: int = 0, length: float = 0, mrt_exp: float = 0, daymet_exp: float = 0, wbgt_exp: float = 0, reroute: int = 0,vulnerable: int = 0):
        self.agent_id = agent_id
        self.trip_id = trip_id
        self.mode = mode
        self.route = route
        self.abm_start = abm_start
        self.duration = duration
        self.length = length
        self.mrt_exp = mrt_exp
        self.daymet_exp = daymet_exp
        self.mrt_exp = mrt_exp
        self.wbgt_exp = wbgt_exp
        self.reroute = reroute
        self.vulnerable = vulnerable

    def dict_id(self):
        return self.trip_id

    def return_values(self) -> tuple:
        # rewrite return_values function in the icarus_obj object
        return (self.agent_id, self.trip_id, self.mode, json.dumps(self.route),self.abm_start, self.duration, self.length, self.mrt_exp, self.daymet_exp, self.wbgt_exp, self.reroute, self.vulnerable)






# import time
# start = time.time()
# for i in range(10000000):
#     temp.return_values()
#     #(temp.osm_id, temp.node1, temp.node2, temp.length)
# print(time.time()-start)