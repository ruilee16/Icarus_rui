# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 15:17:59 2021

@author: ruili
"""

import pandas as pd
agent = pd.read_csv(r'D:\2020 ICARUS\data\agents.csv')
agent = agent.rename(columns={'agent_id': 'agentid', 'household_id': 'hhid', 
                              'household_idx':'pnum'})
agent = agent[['agentid', 'hhid', 'pnum']]
agent.to_csv(r'C:\test_codes_delete_later\agents.csv')


import osmium as osm

class OSMHandler(osm.SimpleHandler):

    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_node_dict = {}
        self.osm_way_dict = {}


    def node(self, n):
        self.osm_node_dict[n.id] =  n.location

    # def way(self, w):
    #     way = Way()
    #     way.osm_way_id = int(w.id)
    #     #way.attr = dict(w.tags)
    #     way.highway = w.tags.get('highway')
    #     way.maxspeed = w.tags.get('maxspeed')
    #     way.foot = w.tags.get('foot')
    #     way.service = w.tags.get('service')
    #     way.access = w.tags.get('access')
    #     way.hov = w.tags.get('hov')
    #     way.ref_node_id_list = [int(node.ref) for node in w.nodes]
    #     # ways contains all street and parking lots informations. on-street parking: residential, unclassified  
    #     if functions._checkIn(way) and functions._checkEx(way):
    #         self.osm_way_dict[way.osm_way_id] = way
        
    # # def relation(self, r):
    # # could generate bus route.
    
    # def cleanup(self):
    #     cleaned_nodes_list = set()
    #     used_nodes = set()
    #     for way_id in self.osm_way_dict:
    #         temp_node_list = self.osm_way_dict[way_id].ref_node_id_list
    #         used_nodes.add(temp_node_list[0])
    #         used_nodes.add(temp_node_list[-1])
    #         cleaned_nodes_list.add(temp_node_list[0])
    #         cleaned_nodes_list.add(temp_node_list[-1]) 
    #         for i in temp_node_list[1:-1]:
    #             if i in used_nodes:
    #                 cleaned_nodes_list.add(i)
    #             else:
    #                 used_nodes.add(i)
    #     # for i in used_nodes:
    #     #     self.osm_node_dict[i].project(4326, 2868)
    #     temp_nodes = {i: self.osm_node_dict[i] for i in used_nodes}
    #     self.cleaned_node_dict =  {i: self.osm_node_dict[i] for i in cleaned_nodes_list}
    #     self.osm_node_dict = temp_nodes
    
osm_handler = OSMHandler()
osm_handler.apply_file(r'C:/test_codes_delete_later/oakland.osm')
