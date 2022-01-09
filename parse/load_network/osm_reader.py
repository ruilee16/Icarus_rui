from shapely.geometry import Point
import osmium as osm
import networkx as nx
import pandas as pd
import geopandas as gpd


def _check_in():
    pass


def _check_ex():
    pass

class Way:
    def __init__(self):
        self.attr = None
        self.osm_way_id = None  # string
        self.highway = None
        self.maxspeed = None
        self.foot = None
        self.service = None
        self.access = None
        self.hov = None
        self.ref_node_id_list = []


# define Node class to hold the node data record from .osm file
class Node:
    __slots__ = ['osm_id', 'geometry']

    def __init__(self, osm_id: int, lon: float, lat: float) -> None:
        """
        create node object
        :param osm_id: openstreetmap node id
        :param lon: logitude
        :param lat: latitude
        """
        self.osm_id = osm_id
        self.geometry = Point(lon, lat)

# define Link class
# def project(self, src_epsg: int, prj_epsg: int):
#     self.geometry = Point(functions.project(self.geometry.x, self.geometry.y, src_epsg, prj_epsg))


class Link:
    # the identifier of links will be the nodes tuple a link connected
    __slots__ = ['node_list', 'osm_id', 'geometry', 'length',
                 'daymet_id', 'mrt_id', 'tree_ratio', 'highway']

    def __init__(self, nodes: tuple):
        self.node_list = nodes
        # self.node_list = tuple(nodes.keys())
        self.geometry = None
        # node = list(nodes.values())
        self.length = None
        # self.length = geodesic((node[0].geometry.y, node[0].geometry.x), (node[1].geometry.y, node[1].geometry.x)).kilometers*1000
        self.osm_id = None
        self.highway = None
        self.daymet_id = None
        self.mrt_id= None
        self.tree_ratio = None

    def to_dict(self):
        return {
            'length': self.length,
            'osm': self.osm_id,
            'geometry': self.geometry,
            'highway': self.highway
        }

    # def parse_mrt(self, buff: float = 0):
    #     buffer = self.geometry.buffer(buff, cap_style=2)
    #     # to parse the enviroment (such as the tree ratio, MRT id, Daymet ids) into the link, parcel. The method I thought about was spatial join
    #     pass


class OSMHandler(osm.SimpleHandler):

    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_node_dict = {}
        self.osm_way_dict = {}
        self.bus_node_dict = {}
        self.cleaned_node_dict = {}

    def node(self, n):
        node = Node(int(n.id), n.location.lon, n.location.lat)
        is_bus = n.tags.get('bus')
        self.osm_node_dict[node.osm_id] = node
        if is_bus == 'yes':
            self.bus_node_dict[node.osm_id] = node

    def way(self, w):
        way = Way()
        way.osm_way_id = int(w.id)
        # way.attr = dict(w.tags)
        way.highway = w.tags.get('highway')
        way.maxspeed = w.tags.get('maxspeed')
        way.foot = w.tags.get('foot')
        way.service = w.tags.get('service')
        way.access = w.tags.get('access')
        way.hov = w.tags.get('hov')
        way.ref_node_id_list = [int(node.ref) for node in w.nodes]
        # ways contains all street and parking lots informations. on-street parking: residential, unclassified
        if _check_in(way) and _check_ex(way):
            self.osm_way_dict[way.osm_way_id] = way

    # def relation(self, r):
    # could generate bus route.

    def cleanup(self):
        cleaned_nodes_list = set()
        used_nodes = set()
        for way_id in self.osm_way_dict:
            temp_node_list = self.osm_way_dict[way_id].ref_node_id_list
            used_nodes.add(temp_node_list[0])
            used_nodes.add(temp_node_list[-1])
            cleaned_nodes_list.add(temp_node_list[0])
            cleaned_nodes_list.add(temp_node_list[-1])
            for i in temp_node_list[1:-1]:
                if i in used_nodes:
                    cleaned_nodes_list.add(i)
                else:
                    used_nodes.add(i)
        # for i in used_nodes:
        #     self.osm_node_dict[i].project(4326, 2868)
        temp_nodes = {i: self.osm_node_dict[i] for i in used_nodes}
        self.cleaned_node_dict = {i: self.osm_node_dict[i] for i in cleaned_nodes_list}
        self.osm_node_dict = temp_nodes
    # def cleanup(self):
    #     cleaned_nodes_list = set()
    #     used_nodes = set()
    #     used_nodes_list = {}
    #     for way_id in self.osm_way_dict:
    #         way = self.osm_way_dict[way_id]
    #         cleaned_nodes_list |= set([way.ref_node_id_list[0],way.ref_node_id_list[-1]])
    #         used_nodes |= set([way.ref_node_id_list[0],way.ref_node_id_list[-1]])
    #         for node in way.ref_node_id_list[1:-1]:
    #             if node in used_nodes:
    #                 cleaned_nodes_list.add(node)
    #             else:
    #                 used_nodes.add(node)
    #     used_nodes_list={node:self.osm_node_dict[node] for node in cleaned_nodes_list}
    #     self.multitime_node = used_nodes_list
    # self.osm_node_dict = cleaned_nodes_list


# def link_from_way(way, nodes, max_link_id):
#     temp_linkDict = {}
#     node_list = way.ref_node_id_list
#     link_id = max_link_id
#     for i in range(0, len(node_list)-1):
#         # (self, osm_id: str, node_list: tuple, mode: list):
#         temp_link = Link(nodes, way.osm_way_id, (node_list[i], node_list[i+1]))
#         temp_linkDict.update({temp_link.link_id: temp_link})


class Network:
    __slots__ = ['links', 'nodes']

    def __init__(self):
        self.links = {}
        self.nodes = {}

    def net_from_osm(self, h: OSMHandler):
        self.nodes = h.cleaned_node_dict
        nodes = h.osm_node_dict
        for item in h.osm_way_dict:
            way = h.osm_way_dict[item]
            nodes_ref = way.ref_node_id_list
            try:
                ini_node = []
                ini_node.append(nodes_ref[0])
                for n in nodes_ref[1:]:
                    ini_node.append(n)
                    if n in self.nodes:
                        link = Link((ini_node[0], ini_node[-1]))
                        _node_list = [nodes[i] for i in ini_node]
                        link.geometry = functions.getLineFromRefNodes(_node_list)
                        link.osm_id = way.osm_way_id
                        link.length = sum(functions.getDistanceFromCoord([_node_list[i], _node_list[i + 1]]) for i in
                                          range(0, len(_node_list) - 1))
                        link.highway = way.highway
                        if link.node_list in self.links:
                            if link.length < self.links[link.node_list].length:
                                self.links[link.node_list] = link
                        else:
                            self.links.update({link.node_list: link})
                        ini_node = [n]

            except:
                pass

    # def _removeIsolated(self,min_nodes):
    #     node_list = list(self.nodes.keys())
    #     node_to_idx_dict = self.nodes
    #     link_list = list(self.links.keys())
    #     number_of_nodes = len(node_list)
    #     node_group_id_list = [-1] * number_of_nodes

    #     group_id = 0
    #     start_idx = 0

    #     while True:
    #         unprocessed_node_list = [node_list[start_idx]]
    #         node_group_id_list[start_idx] = group_id
    #         while unprocessed_node_list:
    #             node = unprocessed_node_list.pop()
    #             for ob_link in node.outgoing_link_list:
    #                 ob_node = ob_link.to_node
    #                 if node_group_id_list[node_to_idx_dict[ob_node]] == -1:
    #                     node_group_id_list[node_to_idx_dict[ob_node]] = group_id
    #                     unprocessed_node_list.append(ob_node)

    #             for ib_link in node.incoming_link_list:
    #                 ib_node = ib_link.from_node
    #                 if node_group_id_list[node_to_idx_dict[ib_node]] == -1:
    #                     node_group_id_list[node_to_idx_dict[ib_node]] = group_id
    #                     unprocessed_node_list.append(ib_node)

    #     unreachable_node_exits = False
    #     for idx in range(start_idx+1,number_of_nodes):
    #         if node_group_id_list[idx] == -1:
    #             unreachable_node_exits = True
    #             break

    #         if unreachable_node_exits:
    #             start_idx = idx
    #             group_id += 1
    #         else:
    #             break

    #     group_id_set = set(node_group_id_list)
    #     group_isolated_dict = {}
    #     for group_id in group_id_set:
    #         group_size = node_group_id_list.count(group_id)
    #         if group_size < min_nodes:
    #             group_isolated_dict[group_id] = True
    #         else:
    #             group_isolated_dict[group_id] = False

    #     removal_link_set = set()
    #     for idx, node in enumerate(node_list):
    #         if group_isolated_dict[node_group_id_list[idx]]:
    #             del self.nodes[node.node_id]
    #             for ob_link in node.outgoing_link_list: removal_link_set.add(ob_link)
    #             for ib_link in node.incoming_link_list: removal_link_set.add(ib_link)
    #     for link in removal_link_set:
    #         del self.links[link.link_id]

    def net_to_nx(self):
        G = nx.Graph()
        G.add_nodes_from(
            [(i, {'x': self.nodes[i].geometry.x, 'y': self.nodes[i].geometry.y}) for i in list(self.nodes)])
        G.add_weighted_edges_from([(*self.links[i].node_list, self.links[i].length) for i in self.links])
        G.graph["crs"] = 'epsg:4326'
        return G

    def net_to_shp(self, url: str):
        if bool(self.links):
            temp = [self.links[link].to_dict() for link in self.links]
            temp = pd.DataFrame(temp)
            gdf = gpd.GeoDataFrame(temp, geometry='geometry', crs='epsg:%s' % 4326)
            gdf.to_file(url, driver='ESRI Shapefile')
